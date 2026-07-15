from datetime import datetime, timezone
from enum import Enum as PythonEnum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RunStatus(str, PythonEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunTrigger(str, PythonEnum):
    UPLOAD = "upload"
    REANALYSIS = "reanalysis"
    MANUAL = "manual"
    SCHEDULED = "scheduled"


class ProcessingRun(Base):
    __tablename__ = "processing_runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    upload_id: Mapped[int] = mapped_column(
        ForeignKey("uploads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[RunStatus] = mapped_column(
        SqlEnum(
            RunStatus,
            values_callable=lambda statuses: [
                status.value for status in statuses
            ],
            native_enum=False,
            create_constraint=True,
            name="run_status",
        ),
        default=RunStatus.RUNNING,
        nullable=False,
        index=True,
    )

    trigger: Mapped[RunTrigger] = mapped_column(
        SqlEnum(
            RunTrigger,
            values_callable=lambda statuses: [
                status.value for status in statuses
            ],
            native_enum=False,
            create_constraint=True,
            name="trigger_status",
        ),
        default=RunTrigger.UPLOAD,
        nullable=False,
        index=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
