import uuid
from sqlalchemy import UUID, Boolean,Column, ForeignKey, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float, DateTime


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    custumer_buyer = Column(UUID, ForeignKey('custumers.id')) # Cliente que comprou o produto
    seller_store = Column(UUID, ForeignKey('stores.id')) # Loja que vendeu o produto
    value = Column(Float) 
    date_time = Column(DateTime) # Data e hora da compra
    percentage_cash = Column(Float) # Porcentagem de cashback que o cliente irá receber em relação ao valor da compra
    cash_generated = Column(UUID, ForeignKey('cashbacks.id')) # Cashback gerado para o cliente pela compra