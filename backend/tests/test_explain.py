from app.services.llm.nodes.explain import explain
from app.models.analysis_result import ExplanationStatus

state = {
    "formatted_context": """
Verdict: Authentic

Confidence: 0.97

Risk Score: 0.05

Agent: vision

Evidence:
- No face inconsistencies detected
- Metadata appears normal

Technical Explanation:
No manipulation artifacts detected.
""",
    "status": ExplanationStatus.PENDING,
}

print("=" * 60)
print("Testing Explain Node")
print("=" * 60)

result = explain(state)

print(result["report"])