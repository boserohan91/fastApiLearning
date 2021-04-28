from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///myblogs.db"

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/test_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()