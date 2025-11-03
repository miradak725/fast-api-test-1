import os 
from fastapi import Depends,FastAPI
from sqlmodel import create_engine, Field, SQLModel,Session
from dotenv import load_dotenv
from typing import Annotated

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# class Records(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str

engine = create_engine(DATABASE_URL,echo=True)

#Initialize database tables
def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
            raise
        finally:
            session.close()


SessionDep=Annotated[Session,Depends(get_session)]
