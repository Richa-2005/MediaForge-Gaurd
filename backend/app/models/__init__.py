from app.database.session import engine
from app.models.base import Base
from app.models.upload import Upload
from app.models.analysis_result import AnalysisResult
from app.models.processing_artifacts import ProcessingArtifact
from app.models.processing_run import ProcessingRun
from app.models.processing_step import ProcessingStep
from app.models.user import User
from app.database.migrations import migrate_database_schema


def create_tables():
    Base.metadata.create_all(bind=engine)
    migrate_database_schema(engine)


if __name__ == "__main__":
    create_tables()
