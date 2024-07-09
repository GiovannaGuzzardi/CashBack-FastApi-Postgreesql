from datetime import datetime
import uuid
from sqlalchemy import UUID, Boolean,Column, ForeignKey, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float, DateTime


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    id_customer = Column(UUID(as_uuid=True), ForeignKey('customers.id', name='fk_sale_customer'))
    id_store = Column(UUID(as_uuid=True), ForeignKey('stores.id', name='fk_sale_store'))
    value = Column(Float) 
    date_time = Column(DateTime, default=datetime.now) # Data e hora da compra

    stores = relationship('Store', back_populates='sale')
    customers = relationship('customer', back_populates='sale')


    cashbacks = relationship('Cashback', back_populates='sale')
    
# class SaleBase(BaseModel):
#     id_sale : UUID
#     id_customer : UUID
#     id_store : UUID 
#     value : float = Field(default=0.0)
#     data_hora : datetime = Field(default_factory=lambda: datetime.now(timezone_brasilia))