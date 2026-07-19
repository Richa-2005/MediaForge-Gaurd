from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.analysis_result import AnalysisResult
from app.models.analysis_result import ExplanationStatus
from app.services.llm.graph import explanation_graph

db = SessionLocal()

analysis = db.scalar(
    select(AnalysisResult)
)

if analysis is None:
    raise RuntimeError(
        "No AnalysisResult exists. Upload one image first."
    )

print("=" * 60)
print("Running LangGraph")
print("=" * 60)

state = explanation_graph.invoke(
    {
        "analysis_id": analysis.id,
        "db": db,
        "status": ExplanationStatus.PENDING,
    }
)

print()

print("Finished.")

updated = db.get(
    AnalysisResult,
    analysis.id,
)

print(updated.summary)
print(updated.explanation_status)