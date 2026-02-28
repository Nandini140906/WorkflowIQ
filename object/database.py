import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#SQLite database configruration
sql_database_url="sqlite:///./workflow.db"

engine=create_engine(sql_database_url,connect_args={"check_same_thread":False})
local_session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

db=local_session()
def get_db():
    try:
        yield db
    finally:
        db.close()

        














































