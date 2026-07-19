from app.models.analysis_result import AgentName, AnalysisResult
from app.schemas.analysis_result import AnalysisResultResponse
from app.services.llm.state import ExplanationState


def collect_context(
    state: ExplanationState,
) -> ExplanationState:

    analysis_row = state["db"].get(
        AnalysisResult,
        state["analysis_id"],
    )

    if analysis_row is None:
        state["analysis_result"] = None
        state["formatted_context"] = None
        return state

    analysis = AnalysisResultResponse.model_validate(
        analysis_row
    )

    state["analysis_result"] = analysis

    agent = analysis.agent.value
    label = analysis.label.value

    visual_available = analysis.agent in {
        AgentName.VISION,
        AgentName.VIDEO,
    }

    audio_available = analysis.agent == AgentName.AUDIO

    
    metadata_available = bool(
        analysis.details
        and analysis.details.get("metadata_analysis")
    )

    evidence_lines: list[str] = []

    for index, evidence in enumerate(
        analysis.evidence or [],
        start=1,
    ):
        method = evidence.get("method", "Unknown method")
        summary = evidence.get(
            "summary",
            "No summary supplied.",
        )
        score = evidence.get("score")
        confidence = evidence.get("confidence")

        evidence_lines.append(
            "\n".join(
                [
                    f"Evidence {index}:",
                    f"- Method: {method}",
                    f"- Observation: {summary}",
                    f"- Method score: {score}",
                    f"- Method confidence: {confidence}",
                ]
            )
        )

    formatted_context = f"""
Media type / forensic agent: {agent}

Final forensic verdict: {label}
Final risk score: {analysis.risk_score:.4f}
Final confidence: {analysis.confidence:.4f}

Applicable report sections:
- Visual analysis: {"available" if visual_available else "not applicable"}
- Audio analysis: {"available" if audio_available else "not applicable"}
- Metadata analysis: {"available" if metadata_available else "not applicable"}

Technical explanation from the forensic engine:
{analysis.explanation or "No technical explanation supplied."}

Forensic evidence:
{chr(10).join(evidence_lines) if evidence_lines else "No evidence supplied."}

Additional analysis details:
{analysis.details or "No additional details supplied."}

Important interpretation rules:
- Method scores are raw outputs from individual forensic techniques.
- A higher method score does not automatically mean stronger evidence of authenticity.
- A higher method score does not automatically mean stronger evidence of manipulation.
- Describe each method only using its supplied observation.
- The final verdict and final confidence are authoritative.
"""

    state["formatted_context"] = formatted_context

    return state


def no_analysis_router(
    state: ExplanationState,
) -> str:
    if state.get("analysis_result") is None:
        return "Abort"

    return "Proceed"