from app.database.session import engine
from app.models.base import Base
from app.models.upload import Upload
from app.models.analysis_result import AnalysisResult

def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
