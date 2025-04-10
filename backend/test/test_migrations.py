import pytest
import os

from sqlalchemy import Engine, create_engine, inspect
from alembic.config import Config
from alembic import command

from testcontainers.postgres import PostgresContainer
from typing import Generator

@pytest.fixture(scope="module")
def postgres_container() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:alpine") as postgres:
        yield postgres


@pytest.fixture(scope="module")
def alembic_config(postgres_container: PostgresContainer) -> Config:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ini_path = os.path.join(base_dir, "..", "alembic.ini")
    config = Config(ini_path)

    db_url = postgres_container.get_connection_url()
    config.set_main_option("sqlalchemy.url", db_url)

    return config

@pytest.fixture(scope="module")
def engine(postgres_container: PostgresContainer) -> Generator[Engine]:
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)
    yield engine
    engine.dispose()

def test_alembic_migrations(alembic_config: Config, engine: Engine) -> None:
    # Run the migrations
    with engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")

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
