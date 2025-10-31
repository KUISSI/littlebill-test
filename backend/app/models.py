# Tes Pydantic models

from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    customers_id = Column(Integer, unique=True, index=True)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer)
    date = Column(String)
    total = Column(Float)
    currency = Column(String)
    store_id = Column(Integer)
    customer_id = Column(Integer)

