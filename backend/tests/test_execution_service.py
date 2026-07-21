from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

from app.models.analysis_result import AgentName
from app.models.processing_run import RunStatus
from app.models.upload import UploadStatus
from app.services import execution_service


def test_complete_processing_uses_supervisor_as_primary(monkeypatch):
    report = Mock()
    monkeypatch.setattr(execution_service, "generate_upload_report", report)
    specialist = SimpleNamespace(
        id=10,
        agent=AgentName.TEXT,
        risk_score=0.9,
    )
    supervisor = SimpleNamespace(
        id=11,
        agent=AgentName.SUPERVISOR,
        risk_score=0.4,
    )
    upload = SimpleNamespace(id=7, status=UploadStatus.PROCESSING)
    running = SimpleNamespace(
        id=5,
        status=RunStatus.RUNNING,
        started_at=datetime.now(timezone.utc).replace(tzinfo=None),
        completed_at=None,
        duration_ms=None,
    )
    db = Mock()

    execution_service.complete_processing(
        [specialist, supervisor], upload, running, db
    )

    report.assert_called_once_with(
        upload_id=7,
        primary_analysis_id=11,
        db=db,
    )
    assert upload.status == UploadStatus.COMPLETED
    assert running.status == RunStatus.COMPLETED


def test_complete_processing_falls_back_to_highest_risk(monkeypatch):
    report = Mock()
    monkeypatch.setattr(execution_service, "generate_upload_report", report)
    results = [
        SimpleNamespace(id=1, agent=AgentName.TEXT, risk_score=0.2),
        SimpleNamespace(id=2, agent=AgentName.FACTCHECK, risk_score=0.8),
    ]
    upload = SimpleNamespace(id=7, status=UploadStatus.PROCESSING)
    running = SimpleNamespace(
        id=5,
        status=RunStatus.RUNNING,
        started_at=datetime.now(timezone.utc).replace(tzinfo=None),
        completed_at=None,
        duration_ms=None,
    )
    db = Mock()

    execution_service.complete_processing(results, upload, running, db)

    assert report.call_args.kwargs["primary_analysis_id"] == 2
