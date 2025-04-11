from typing import Generator
from sqlalchemy.orm.session import Session
from config.environment import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = get_settings()

engine = create_engine(str(settings.db_url), future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Generator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
