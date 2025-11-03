from app.db.db import SessionDep
from app.models.token_usage import TokenUsage
from sqlmodel import select
from datetime import datetime
from core.logger import logger




class TokenService:
    def __init__(self, monthly_limit: int = 10000):
        self.MONTHLY_TOKEN_LIMIT = monthly_limit
   
    # get_token_count
    def get_token_count(self, user_id: int, session) -> TokenUsage:
        """Retrieve token count for a specific user."""
        try:
            statement = select(TokenUsage).where(TokenUsage.user_id == user_id)
            record = session.exec(statement).first()
            if record:
                logger.info(f"Retrieved token count for user_id={user_id}: {record.tokens_used} used, {record.remaining_tokens} remaining")
            else:
                logger.info(f"No token record found for user_id={user_id}")
            return record
        except Exception as e:
            logger.error(f"Error retrieving token count for user_id={user_id}: {e}")
            return None

    # set_token_count
    def set_token_count(self, user_id: int, month:int,tokens_used:int, session: SessionDep) ->  TokenUsage:
        """Create or update token count for a specific user and month."""
        statement = select(TokenUsage).where(TokenUsage.user_id == user_id,TokenUsage.month == month)
        record = session.exec(statement).first()

        if record:
             # Increment existing usage
            record.tokens_used += tokens_used
             # Recalculate remaining tokens
            record.remaining_tokens = max(
                self.MONTHLY_TOKEN_LIMIT - record.tokens_used, 0
            )
            record.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            session.add(record)
            logger.info(f"Updated token count for user_id={user_id}, month={month}")
            
        else:
            #Create new record
            remaining_tokens = max(self.MONTHLY_TOKEN_LIMIT - tokens_used, 0)
            #create new record
            new_record = TokenUsage(
                user_id = user_id,
                month = month,
                tokens_used = tokens_used,
                remaining_tokens = self.MONTHLY_TOKEN_LIMIT - tokens_used,
                updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            )
            session.add(new_record)
        session.commit()
        session.refresh(record if record else new_record)
        logger.info(f"Token count set for user_id={user_id}, month={month}: tokens_used={tokens_used}, remaining_tokens={record.remaining_tokens if record else new_record.remaining_tokens}")

        return record or new_record

# @router.get("/{user_id}")
# def read_token_count(user_id: int, session: Session = Depends(get_session)):
#     count = get_token_count(session, user_id)
#     return {"user_id": user_id, "token_count": count}

# @router.post("/{user_id}")
# def update_token_count(user_id: int, new_count: int, session: Session = Depends(get_session)):
#     record = set_token_count(session, user_id, new_count)
#     return {"message": "Token count updated successfully", "data": record.token_count}


# from sqlmodel import Session, select
# from app.models.token_model import TokenUsage

# def get_token_count(session: Session, user_id: int) -> int:
#     statement = select(TokenUsage).where(TokenUsage.user_id == user_id)
#     result = session.exec(statement).first()
#     return result.token_count if result else 0

# def set_token_count(session: Session, user_id: int, new_count: int) -> TokenUsage:
#     statement = select(TokenUsage).where(TokenUsage.user_id == user_id)
#     record = session.exec(statement).first()
    
#     if record:
#         record.token_count = new_count
#     else:
#         record = TokenUsage(user_id=user_id, token_count=new_count)
#         session.add(record)
    
#     session.commit()
#     session.refresh(record)
#     return record