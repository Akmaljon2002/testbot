from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(30))
    telefon = Column(String(15))
    user_id = Column(BigInteger, unique=True)
    role = Column(String(20), default='user')
    joined_date = Column(DateTime, default=datetime.now())

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    text = Column(String(50))
    created_at = Column(DateTime, default=datetime.now())
