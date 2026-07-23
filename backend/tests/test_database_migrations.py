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


def test_legacy_upload_hash_constraint_is_migrated(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'legacy_uploads.db'}")
    User.__table__.create(engine)

    with engine.begin() as connection:
        connection.exec_driver_sql(
            """
            CREATE TABLE uploads (
                id INTEGER NOT NULL,
                user_id INTEGER,
                original_filename VARCHAR(255) NOT NULL,
                stored_filename VARCHAR(255) NOT NULL,
                file_path VARCHAR(1000) NOT NULL,
                media_type VARCHAR(50) NOT NULL,
                mime_type VARCHAR(100) NOT NULL,
                file_size BIGINT NOT NULL,
                sha256_hash VARCHAR(64) NOT NULL,
                status VARCHAR(10) NOT NULL,
                language VARCHAR(20),
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                PRIMARY KEY (id),
                UNIQUE (stored_filename),
                UNIQUE (sha256_hash)
            )
            """
        )

    migrate_database_schema(engine)

    with engine.connect() as connection:
        table_sql = connection.scalar(
            text(
                "SELECT sql FROM sqlite_master "
                "WHERE type='table' AND name='uploads'"
            )
        )
        unique_constraints = inspect(connection).get_unique_constraints(
            "uploads"
        )

    assert "UNIQUE (sha256_hash)" not in table_sql
    assert any(
        item["column_names"] == ["user_id", "sha256_hash"]
        for item in unique_constraints
    )
