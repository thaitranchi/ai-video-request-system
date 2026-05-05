from typing import Generator
from app.db.session import db_session

def get_db() -> Generator:
    # For this prototype, we return a simple in-memory session
    yield db_session