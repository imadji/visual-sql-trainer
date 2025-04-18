from sqlalchemy import Column, Integer, String, Float
from .database import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True)
    db_login = Column(String(50), unique=True)
    password = Column(String(128))
    db_password = Column(String(128))
