import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..main import app
from passlib.context import CryptContext

from ..database import Base  
from ..routers import auth,todos
from ..models import Todos,Users


SQL_DATABASE = "sqlite:///./testdb.db"        # file‑based SQLite for determinism
engine = create_engine(
    SQL_DATABASE,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,                    # one shared connection
)

bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')

TestingSessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False
)

# Create the tables **before** any test runs
Base.metadata.create_all(bind=engine)

# ===== 3️⃣  Dependency overrides =====
def override_get_current_user() -> dict:
    """Fake authenticated user."""
    return {"username": "xyz", "id": 1, "user_role": "admin"}

def override_get_db():
    """Return a session that talks to the test database."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
client = TestClient(app)

# ===== 4️⃣  Test fixtures =====
@pytest.fixture
def dummy_todo():
    """Create one Todo in the test DB and delete it afterwards."""
    with TestingSessionLocal() as db:
        todo1 = Todos(
            title="Learn to code!!",
            description="It's about coding!!",
            priority=4,
            complete=False,
            owner_id=1,              # must match the fake user id
        )
        db.add(todo1)
        db.commit()
        db.refresh(todo1)          # so that todo.id is set

    # Yield the record before the test accesses it
    yield todo1

    # ---- cleanup -------------------------------------------------
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()
        
@pytest.fixture
def dummy_user():
    db = TestingSessionLocal()
    user1 = Users(
        email="xyzMike.com",
        username="Mike",
        first_name="xyz", 
        last_name="Mike",
        hashed_passwprd=bcrypt_context.hash("pass123"),  # Fixed typo
        is_active=True,
        role="",
        phone_number="9724663588"
    )
    
    db.add(user1)
    db.commit()
    
    yield user1
    
    # Cleanup
    db.query(Users).filter(Users.id == user1.id).delete()
    db.commit()
    db.close()