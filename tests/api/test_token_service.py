import pytest
from sqlmodel import Session, SQLModel, create_engine
from datetime import datetime
from app.models.token_usage import TokenUsage
from app.service.token_service import TokenService 
from sqlmodel import select 

@pytest.fixture
def session():
    """Creaate an in-memory SQLite test database."""
    engine = create_engine("postgresql://postgres:password@localhost:5432/chatbot_test_db")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def token_service():
    """Provide a TokenService instance."""
    return TokenService(monthly_limit=10000)


def test_set_token_count_new_record(token_service,session):
    """Test set_token_count function.
       Creates a new record if none exists """
    user_id= 1
    tokens_used = 100
    month=datetime.utcnow().month
    record=token_service.set_token_count(user_id,month,tokens_used,session)
    statement = select(TokenUsage).where(TokenUsage.user_id == user_id, TokenUsage.month == month)
    
    record_before = session.exec(statement).first()
    existing_tokens = record_before.tokens_used
    
    assert record.tokens_used == tokens_used + existing_tokens
    assert record.user_id == user_id
    assert record.month == month

def test_set_token_count_updates_existing_record(token_service,session):
    """Test set_token_count_function.
       Updates a record if already exists """
    user_id= 1
    token_count = 300
    month=datetime.utcnow().month
    record=token_service.set_token_count(user_id,month,token_count,session)

    assert record.id is not None
    assert record.token_count == token_count
    assert record.user_id == user_id
    assert record.month == month


def test_get_token_count(token_service,session):
    """Test get_token_count """
    user_id= 1
    month=datetime.utcnow().month   
    record=token_service.get_token_count(user_id,session)

    user_id = 1
    month = datetime.utcnow().month

   
    new_record = TokenUsage(
        user_id=user_id,
        month=month,
        tokens_used=200,
        remaining_tokens=9800,
        updated_at=datetime.utcnow()
    )
    session.add(new_record)
    session.commit()

   
    record = token_service.get_token_count(user_id, session)

   
    assert record is not None
    assert record.user_id == user_id
    assert record.month == month
    assert record.tokens_used == 200
    assert record.remaining_tokens == 9800
