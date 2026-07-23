from sqlalchemy import create_engine, inspect, text
from sqlalchemy.schema import CreateTable

from app.database.migrations import migrate_database_schema
from app.models.analysis_result import AnalysisResult
from app.models.upload import Upload
from app.models.user import User


def test_legacy_analysis_constraints_are_migrated(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'legacy.db'}")
    User.__table__.create(engine)
    Upload.__table__.create(engine)
    current_ddl = str(CreateTable(AnalysisResult.__table__).compile(engine))
    legacy_ddl = current_ddl.replace(
        "'text', 'factcheck', 'supervisor'",
        "'text', 'supervisor'",
    ).replace(
        "'authentic', 'manipulated', 'uncertain'",
        "'authentic', 'manipulated', 'misleading', "
        "'uncertain', 'pending'",
    )

    with engine.begin() as connection:
        connection.exec_driver_sql(legacy_ddl)

    migrate_database_schema(engine)

    with engine.connect() as connection:
        migrated_ddl = connection.scalar(
            text(
                "SELECT sql FROM sqlite_master "
                "WHERE type='table' AND name='analysis_results'"
            )
        )
        unique_constraints = inspect(
            connection
        ).get_unique_constraints("analysis_results")

    assert "'factcheck'" in migrated_ddl
    label_constraint = migrated_ddl.split(
        "CONSTRAINT label CHECK", 1
    )[1].split("CONSTRAINT explanation_status", 1)[0]
    assert "'misleading'" not in label_constraint
    assert "'pending'" not in label_constraint
    assert any(
        item["column_names"] == ["upload_id", "agent"]
        for item in unique_constraints
    )
