from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.analysis_result import AnalysisResult
from app.services.llm.report_service import generate_report

db = SessionLocal()

analysis = db.scalar(
    select(AnalysisResult)
)

if analysis is None:
    raise RuntimeError(
        "No analysis result exists."
    )

print("=" * 60)
print("Testing Report Service")
print("=" * 60)

generate_report(
    analysis.id,
    db,
)

analysis = db.get(
    AnalysisResult,
    analysis.id,
)

print()

print("Status :", analysis.explanation_status)
print("Summary :", analysis.summary)