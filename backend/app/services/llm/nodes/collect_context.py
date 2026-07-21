from sqlalchemy import select

from app.models.analysis_result import AnalysisResult
from app.schemas.analysis_result import (
    AnalysisResultResponse,
)
from app.services.llm.state import ExplanationState


def collect_context(
    state: ExplanationState,
) -> ExplanationState:
    db = state["db"]
    upload_id = state["upload_id"]
    primary_analysis_id = state[
        "primary_analysis_id"
    ]

    rows = db.scalars(
        select(AnalysisResult)
        .where(
            AnalysisResult.upload_id == upload_id
        )
        .order_by(AnalysisResult.id)
    ).all()

    if not rows:
        state["analysis_results"] = []
        state["primary_analysis"] = None
        state["formatted_context"] = None
        return state

    analyses = [
        AnalysisResultResponse.model_validate(row)
        for row in rows
    ]

    primary_analysis = next(
        (
            analysis
            for analysis in analyses
            if analysis.id == primary_analysis_id
        ),
        None,
    )

    if primary_analysis is None:
        state["analysis_results"] = analyses
        state["primary_analysis"] = None
        state["formatted_context"] = None
        return state

    context_sections: list[str] = []

    for analysis in analyses:
        evidence_lines: list[str] = []

        for index, evidence in enumerate(
            analysis.evidence or [],
            start=1,
        ):
            evidence_lines.append(
                "\n".join(
                    [
                        f"Evidence {index}:",
                        (
                            "- Method: "
                            f"{evidence.get('method', 'Unknown')}"
                        ),
                        (
                            "- Observation: "
                            f"{evidence.get('summary', 'Not supplied')}"
                        ),
                        (
                            "- Method score: "
                            f"{evidence.get('score')}"
                        ),
                        (
                            "- Method confidence: "
                            f"{evidence.get('confidence')}"
                        ),
                    ]
                )
            )

        agent = (
            analysis.agent.value
            if hasattr(analysis.agent, "value")
            else str(analysis.agent)
        )

        label = (
            analysis.label.value
            if hasattr(analysis.label, "value")
            else str(analysis.label)
        )

        context_sections.append(
            f"""
Agent: {agent}
Analysis ID: {analysis.id}

Verdict: {label}
Risk score: {analysis.risk_score:.4f}
Confidence: {analysis.confidence:.4f}

Technical explanation:
{analysis.explanation or "No explanation supplied."}

Evidence:
{chr(10).join(evidence_lines) if evidence_lines else "No evidence supplied."}

Additional details:
{analysis.details or "No additional details supplied."}
""".strip()
        )

    primary_agent = (
        primary_analysis.agent.value
        if hasattr(primary_analysis.agent, "value")
        else str(primary_analysis.agent)
    )

    formatted_context = f"""
This report combines all analysis results produced for upload
{upload_id}.

The authoritative primary result is:

Primary agent: {primary_agent}
Primary verdict: {primary_analysis.label.value}
Primary risk score: {primary_analysis.risk_score:.4f}
Primary confidence: {primary_analysis.confidence:.4f}

The primary verdict and confidence must not be changed.

All available agent results:

========================================

{chr(10).join(context_sections)}

========================================

Interpretation rules:

- Prefer the primary/supervisor result for the overall verdict.
- Explain each specialist result separately.
- Do not invent evidence or relationships between findings.
- Mention agreement or disagreement only when supported by the results.
- Individual method scores are not overall confidence scores.
- Failed or unavailable agents must not be represented as completed.
- Do not expose file paths or internal implementation details.
""".strip()

    state["analysis_results"] = analyses
    state["primary_analysis"] = primary_analysis
    state["formatted_context"] = formatted_context

    return state

def no_analysis_router(
    state: ExplanationState,
) -> str:
    if not state.get("analysis_results"):
        return "Abort"

    if state.get("primary_analysis") is None:
        return "Abort"

    return "Proceed"