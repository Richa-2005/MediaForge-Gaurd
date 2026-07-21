import logging

from sqlalchemy import Engine, inspect, text


logger = logging.getLogger(__name__)


def migrate_database_schema(engine: Engine) -> None:
    """Apply small idempotent migrations for installations without Alembic."""
    if engine.dialect.name != "sqlite":
        return

    _migrate_sqlite_analysis_results(engine)


def _migrate_sqlite_analysis_results(engine: Engine) -> None:
    from app.models.analysis_result import AnalysisResult

    with engine.connect() as connection:
        table_sql = connection.scalar(
            text(
                "SELECT sql FROM sqlite_master "
                "WHERE type = 'table' AND name = 'analysis_results'"
            )
        )

        if table_sql is None:
            return

        has_current_agents = "'factcheck'" in table_sql
        has_current_labels = (
            "'misleading'" not in table_sql
            and "'pending'" not in _label_constraint(table_sql)
        )
        unique_constraints = inspect(connection).get_unique_constraints(
            "analysis_results"
        )
        has_agent_uniqueness = any(
            constraint.get("column_names") == ["upload_id", "agent"]
            for constraint in unique_constraints
        )

        if (
            has_current_agents
            and has_current_labels
            and has_agent_uniqueness
        ):
            return

        duplicate = connection.execute(
            text(
                "SELECT upload_id, agent, COUNT(*) AS row_count "
                "FROM analysis_results "
                "GROUP BY upload_id, agent "
                "HAVING COUNT(*) > 1 LIMIT 1"
            )
        ).first()
        if duplicate is not None:
            raise RuntimeError(
                "Cannot migrate analysis_results while duplicate "
                "upload/agent rows exist: "
                f"upload_id={duplicate.upload_id}, agent={duplicate.agent}."
            )

        connection.commit()
        connection.exec_driver_sql("PRAGMA foreign_keys=OFF")
        connection.commit()

        try:
            with connection.begin():
                connection.exec_driver_sql(
                    "ALTER TABLE analysis_results "
                    "RENAME TO _analysis_results_old"
                )
                connection.exec_driver_sql(
                    "DROP INDEX IF EXISTS ix_analysis_results_agent"
                )
                connection.exec_driver_sql(
                    "DROP INDEX IF EXISTS ix_analysis_results_upload_id"
                )

                AnalysisResult.__table__.create(connection)

                column_names = [
                    column.name
                    for column in AnalysisResult.__table__.columns
                ]
                quoted_columns = ", ".join(
                    f'"{name}"' for name in column_names
                )
                selected_columns = ", ".join(
                    (
                        "CASE WHEN label IN ('misleading', 'pending') "
                        "THEN 'uncertain' ELSE label END AS label"
                        if name == "label"
                        else f'"{name}"'
                    )
                    for name in column_names
                )
                connection.exec_driver_sql(
                    "INSERT INTO analysis_results "
                    f"({quoted_columns}) "
                    f"SELECT {selected_columns} "
                    "FROM _analysis_results_old"
                )
                connection.exec_driver_sql(
                    "DROP TABLE _analysis_results_old"
                )

            logger.info(
                "Migrated analysis_results constraints to current schema."
            )
        finally:
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")
            connection.commit()


def _label_constraint(table_sql: str) -> str:
    marker = "CONSTRAINT label CHECK"
    start = table_sql.find(marker)
    if start == -1:
        return ""
    end = table_sql.find(")", start)
    return table_sql[start:end]
