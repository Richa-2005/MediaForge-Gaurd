from unittest.mock import Mock

from app.models.analysis_result import ExplanationStatus
from app.services.llm import report_service


def test_generate_upload_report_passes_consolidated_identifiers(monkeypatch):
    invoke = Mock(return_value={"status": ExplanationStatus.COMPLETED})
    monkeypatch.setattr(report_service.explanation_graph, "invoke", invoke)
    db = Mock()

    result = report_service.generate_upload_report(
        upload_id=7,
        primary_analysis_id=11,
        db=db,
    )

    assert result == {"status": ExplanationStatus.COMPLETED}
    state = invoke.call_args.args[0]
    assert state["upload_id"] == 7
    assert state["primary_analysis_id"] == 11
    assert state["db"] is db
