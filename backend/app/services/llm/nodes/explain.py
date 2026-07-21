from app.core.llm_factory import get_chat_model
from app.services.llm.schemas import ExplanationReport
from app.services.llm.state import ExplanationState


def explain(
    state: ExplanationState,
) -> ExplanationState:
    context = state.get("formatted_context")
    primary_analysis = state.get(
        "primary_analysis"
    )

    if context is None:
        raise ValueError(
            "Formatted forensic context is missing."
        )

    if primary_analysis is None:
        raise ValueError(
            "Primary analysis result is missing."
        )

    llm = get_chat_model()

    structured_llm = llm.with_structured_output(
        ExplanationReport
    )

    report = structured_llm.invoke(
        build_explanation_prompt(context)
    )

    report.verdict.label = (
        primary_analysis.label.value
    )
    report.verdict.confidence = (
        primary_analysis.confidence
    )

    state["report"] = report

    return state

def build_explanation_prompt(
    context: str,
) -> str:
    return f"""
You are MediaForge Guard's Report Generation Agent.

Multiple forensic agents may have analyzed the same upload.

Your responsibility is to explain all supplied results in one
consolidated report. You do not choose or modify the final
verdict.

Strict rules:

1. Copy the primary verdict exactly.
2. Copy the primary confidence exactly.
3. Prefer the supervisor result when it is designated primary.
4. Never invent evidence, sources, methods, or conclusions.
5. Explain every available agent result separately.
6. Do not create sections for agents that are not supplied.
7. Do not treat individual method scores as overall confidence.
8. Do not claim findings agree or conflict unless supported.
9. Use cautious language.
10. Never describe the result as proven or definitive.
11. Do not expose file-system paths or implementation details.
12. State important limitations and missing analysis coverage.

Field requirements:

title:
Use "MediaForge Guard Authenticity Report".

verdict:
Copy the supplied primary verdict and confidence exactly.

summary:
One sentence, at most 30 words. Mention the verdict and use
cautious language.

executive_summary:
Write 3 to 5 plain-language sentences summarizing the combined
assessment and strongest supplied observations.

agent_analyses:
Create one entry for every supplied agent result.

For each entry:
- agent must match the supplied agent name.
- title should be a readable section title.
- analysis must explain only that agent's supplied findings.
- key_observations must contain concise supported observations.

key_findings:
Provide 3 to 8 findings drawn from all available agents.

limitations:
Mention uncertainty, possible false positives or false negatives,
and unavailable analysis types where relevant.

recommendation:
Provide practical verification advice.

technical_notes:
Explain how the primary result relates to the specialist results
without inventing fusion logic.

Forensic context:

====================

{context}

====================
"""