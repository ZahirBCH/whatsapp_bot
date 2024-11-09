from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    departure_city = Column(String)
    delivery_city = Column(String)
    weight = Column(Float)