from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from medly_backend.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
