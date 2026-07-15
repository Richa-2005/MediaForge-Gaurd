import enum
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import DateTime, Enum, Float, ForeignKey,Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AgentName(str, enum.Enum):
    VISION = "vision"
    AUDIO = "audio"
    TEXT = "text"
    SUPERVISOR = "supervisor"


class Labels(str, enum.Enum):
    AUTHENTIC = "authentic"
    MANIPULATED ="manipulated"
    MISLEADING = "misleading"
    UNCERTAIN = "uncertain"
    PENDING = "pending"


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    upload_id: Mapped[int] = mapped_column(
        ForeignKey("uploads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    agent: Mapped[AgentName] = mapped_column(
        Enum(
            AgentName,
            values_callable=lambda names: [
                name.value for name in names
            ],
            native_enum=False,
            create_constraint=True,
            name="agent_name",
        ),
        default=AgentName.SUPERVISOR,
        nullable=False,
        index=True,
    )

    label: Mapped[Labels] = mapped_column(
        Enum(
            Labels,
            values_callable=lambda labels: [
                label.value for label in labels
            ],
            native_enum=False,
            create_constraint=True,
            name="label",
        ),
        nullable=False,
    )

    risk_score: Mapped[float] = mapped_column(Float, nullable=False)

    confidence:  Mapped[float] = mapped_column(Float, nullable=False)

    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    evidence: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)

    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

