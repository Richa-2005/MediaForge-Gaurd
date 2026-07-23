import enum
from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class UploadStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Upload(Base):
    __tablename__ = "uploads"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "sha256_hash",
            name="uq_upload_user_sha256",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    original_filename: Mapped[str] = mapped_column(String(255))
    stored_filename: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    file_path: Mapped[str] = mapped_column(String(1000))
    media_type: Mapped[str] = mapped_column(String(50))
    mime_type: Mapped[str] = mapped_column(String(100))
    file_size: Mapped[int] = mapped_column(BigInteger)

    sha256_hash: Mapped[str] = mapped_column(
        String(64),
        index=True,
    )

    status: Mapped[UploadStatus] = mapped_column(
        Enum(
            UploadStatus,
            values_callable=lambda statuses: [
                status.value for status in statuses
            ],
            native_enum=False,
            create_constraint=True,
            name="upload_status",
        ),
        default=UploadStatus.UPLOADED,
        nullable=False,
        index=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
