import enum
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import BigInteger, DateTime, Enum, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class ProcessingArtifact(Base):
    __tablename__ = "processing_artifact"

    id : Mapped[int] = mapped_column(primary_key=True)

    upload_id : Mapped[int] = mapped_column(
        ForeignKey("uploads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    artifact_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    ) 

    file_path : Mapped[str | None] = mapped_column(String(255))

    details : Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    

    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )