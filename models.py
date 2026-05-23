from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Basket(Base):
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True)
    id_doc = Column(String(100))
    goods_json = Column(String(5000))
    doc_date = Column(DateTime, nullable=True)