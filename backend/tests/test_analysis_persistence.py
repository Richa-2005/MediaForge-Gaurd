from types import SimpleNamespace
import sys
import types

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.models.analysis_result import AnalysisResult
from app.models.base import Base
from app.models.processing_artifacts import ProcessingArtifact
from app.models.upload import Upload
from app.services import analysis_service
from src.schemas.agent_result import AgentResult
from src.schemas.analysis_result import AnalysisResult as WorkerAnalysis


def worker_result(agent, risk, confidence):
    return AgentResult(
        upload_id=1,
        agent=agent,
        analysis=WorkerAnalysis(
            label="uncertain",
            risk_score=risk,
            confidence=confidence,
            explanation=f"{agent} result",
            evidence=[],
        ),
    )


class TextAnalysisAgent:
    def analyze(self, *_args, **_kwargs):
        return {
            "text": worker_result("text", 0.2, 0.8),
            "factcheck": worker_result("factcheck", 0.5, 0.4),
            "fusion": worker_result("supervisor", 0.35, 0.6),
        }


def test_run_analysis_is_atomic_and_idempotent(monkeypatch, tmp_path):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    text_path = tmp_path / "sample.txt"
    text_path.write_text("A sample claim.", encoding="utf-8")
    fake_module = types.ModuleType("ai_workers.src.agents.analysis_agent")
    fake_module.AnalysisAgent = TextAnalysisAgent
    monkeypatch.setitem(
        sys.modules,
        "ai_workers.src.agents.analysis_agent",
        fake_module,
    )

    with Session(engine) as db:
        upload = Upload(
            original_filename="sample.txt",
            stored_filename="stored.txt",
            file_path=str(text_path),
            media_type="text",
            mime_type="text/plain",
            file_size=text_path.stat().st_size,
            sha256_hash="a" * 64,
        )
        db.add(upload)
        db.commit()
        db.refresh(upload)
        db.add(
            ProcessingArtifact(
                upload_id=upload.id,
                artifact_type="processed_text",
                file_path=str(text_path),
                details={},
            )
        )
        db.commit()

        first = analysis_service.run_analysis(upload, db)
        second = analysis_service.run_analysis(upload, db)

        count = db.scalar(
            select(func.count()).select_from(AnalysisResult)
        )
        assert len(first) == 3
        assert len(second) == 3
        assert count == 3
