import uuid
from sqlalchemy import UUID, Boolean,Column, ForeignKey, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float, DateTime


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    custumer_buyer = Column(String, ForeignKey('custumers.id'))
    seller_store = Column(String, ForeignKey('stores.id'))
    value = Column(Float)
    date_time = Column(DateTime)
    percentage_cash = Column(Float)
    cash_generated = Column(String, ForeignKey('cashbacks.id'))