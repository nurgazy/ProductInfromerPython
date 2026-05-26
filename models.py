from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Basket(Base):
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True)
    id_doc = Column(String(100))
    goods_json = Column(String(5000))
    doc_date = Column(DateTime, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    role = Column(String(20), default="manager")  # admin, manager, mobile_app
    api_token = Column(String(100), unique=True, nullable=True)