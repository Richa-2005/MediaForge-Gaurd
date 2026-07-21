from app.services.llm.state import ExplanationState


def format_markdown(
    state: ExplanationState,
) -> ExplanationState:
    report = state.get("report")

    if report is None:
        raise ValueError(
            "Explanation report is missing."
        )

    confidence = report.verdict.confidence

    if confidence < 0.50:
        confidence_level = "Low"
    elif confidence < 0.80:
        confidence_level = "Moderate"
    else:
        confidence_level = "High"

    markdown = f"""
# {report.title}

---

## Overall Verdict

**Result:** {report.verdict.label.title()}

**Confidence:** {confidence:.2%} ({confidence_level})

---

## Summary

{report.summary}

---

## Executive Summary

{report.executive_summary}

---

## Agent Analysis
""".strip()

    for section in report.agent_analyses:
        markdown += f"""

### {section.title}

**Agent:** `{section.agent}`

{section.analysis}

#### Key Observations
"""

        if section.key_observations:
            for observation in section.key_observations:
                markdown += f"\n- {observation}"
        else:
            markdown += "\n- No observations supplied."

    markdown += """

---

## Combined Key Findings
"""

    for finding in report.key_findings:
        markdown += f"\n- {finding}"

    markdown += f"""

---

## Recommendation

{report.recommendation}

---

## Limitations

{report.limitations}

---

## Technical Notes

{report.technical_notes}
"""

    state["report_markdown"] = markdown.strip()

    return state