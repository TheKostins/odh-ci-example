from sqlalchemy import Engine, inspect
from alembic.config import Config

def test_alembic_migrations(alembic_config: Config, engine: Engine) -> None:
    # Check if the tables exist
    inspector = inspect(engine)
    expected_tables = ["topics", "messages"]
    for table in expected_tables:
        assert table in inspector.get_table_names()

    # Check if the columns exist in the tables
    topics_expected_columns = set(["id", "name"])
    topics_actual_columns = set(column["name"] for column in inspector.get_columns("topics"))
    assert topics_expected_columns == topics_actual_columns

    messages_expected_columns = set(["id", "author_nickname", "content", "topic_id", "time_created"])
    messages_actual_columns = set(column["name"] for column in inspector.get_columns("messages"))
    assert messages_expected_columns == messages_actual_columns
