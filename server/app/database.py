from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://root:root@db:5432/umom_db"
)

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://root:root@localhost:5430/umom_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS tasks_schema"))
    connection.commit()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
