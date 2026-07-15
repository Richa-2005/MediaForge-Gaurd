from datetime import datetime, timezone
from enum import Enum as PythonEnum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class StepStatus(str, PythonEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    PENDING = "pending"


class ProcessingStep(Base):
    __tablename__ = "processing_steps"

    id: Mapped[int] = mapped_column(primary_key=True)

    processing_run_id: Mapped[int] = mapped_column(
        ForeignKey("processing_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    step_name: Mapped[str] = mapped_column(String(100), nullable=False)

    status: Mapped[StepStatus] = mapped_column(
        SqlEnum(
            StepStatus,
            values_callable=lambda statuses: [
                status.value for status in statuses
            ],
            native_enum=False,
            create_constraint=True,
            name="step_status",
        ),
        default=StepStatus.PENDING,
        nullable=False,
        index=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
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
