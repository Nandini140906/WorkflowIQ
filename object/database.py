import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

sql_database_url = os.getenv("DATABASE_URL", "sqlite:///./workflow.db")

if sql_database_url.startswith("postgres://"):
    sql_database_url = sql_database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(sql_database_url)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()