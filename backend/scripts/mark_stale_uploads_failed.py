from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.processing_run import ProcessingRun, RunStatus
from app.models.processing_step import ProcessingStep, StepStatus
from app.models.upload import Upload, UploadStatus


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mark stale queued/processing uploads as failed.",
    )
    parser.add_argument(
        "--older-than-minutes",
        type=int,
        default=15,
        help="Only touch uploads updated before this many minutes ago.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes. Without this flag, only prints matching IDs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(
        minutes=args.older_than_minutes,
    )

    with SessionLocal() as db:
        uploads = db.scalars(
            select(Upload).where(
                Upload.status.in_(
                    [
                        UploadStatus.QUEUED,
                        UploadStatus.PROCESSING,
                    ]
                ),
                Upload.updated_at < cutoff,
            )
        ).all()

        if not uploads:
            print("No stale queued/processing uploads found.")
            return

        upload_ids = [upload.id for upload in uploads]
        print(f"Found stale uploads: {upload_ids}")

        if not args.apply:
            print("Dry run only. Re-run with --apply to mark them failed.")
            return

        now = datetime.now(timezone.utc)
        for upload in uploads:
            upload.status = UploadStatus.FAILED
            upload.updated_at = now

        runs = db.scalars(
            select(ProcessingRun).where(
                ProcessingRun.upload_id.in_(upload_ids),
                ProcessingRun.status == RunStatus.RUNNING,
            )
        ).all()
        for run in runs:
            run.status = RunStatus.FAILED
            run.completed_at = now

        run_ids = [run.id for run in runs]
        if run_ids:
            steps = db.scalars(
                select(ProcessingStep).where(
                    ProcessingStep.processing_run_id.in_(run_ids),
                    ProcessingStep.status.in_(
                        [
                            StepStatus.PENDING,
                            StepStatus.RUNNING,
                        ]
                    ),
                )
            ).all()
            for step in steps:
                step.status = StepStatus.FAILED
                step.completed_at = now
                step.error_message = (
                    "Marked failed during stale queued upload cleanup."
                )

        db.commit()
        print(f"Marked {len(upload_ids)} stale uploads as failed.")


if __name__ == "__main__":
    main()
