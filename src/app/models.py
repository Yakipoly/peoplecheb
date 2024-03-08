from sqlalchemy import Column, String, Integer
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
