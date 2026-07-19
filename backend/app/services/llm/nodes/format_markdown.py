from app.services.llm.state import ExplanationState


def format_markdown(
    state: ExplanationState,
) -> ExplanationState:

    report = state["report"]
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

## Verdict

**Result:** {report.verdict.label.title()}

**Confidence:** {confidence:.2%} ({confidence_level})

---

## Summary

{report.summary}

---

## Executive Summary

{report.executive_summary}

---

## Analysis

### Visual Analysis

{report.analysis.visual_analysis}

### Audio Analysis

{report.analysis.audio_analysis}

### Metadata Analysis

{report.analysis.metadata_analysis}

---

## Key Findings

"""

    for finding in report.key_findings:
        markdown += f"- {finding}\n"

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

    state["report_markdown"] = markdown

    return state