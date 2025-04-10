import pytest
import os

from alembic.config import Config
from alembic import command

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

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
def engine(postgres_container: PostgresContainer, alembic_config: Config) -> Generator[Engine]:
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)

    # Run the migrations
    with engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")

    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def session_mk(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)

@pytest.fixture(scope="function")
def session(session_mk: sessionmaker[Session]) -> Generator[Session]:
    with session_mk() as session:
       yield session
