import uuid
from sqlalchemy import UUID, Boolean,Column, ForeignKey, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    cpf= Column(String, index=True, unique= True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, nullable=True)
    telefone = Column(String, unique =True)

    customer_stores = relationship("CustomerStoreAssociation", back_populates="customer")
    sale = relationship('Sale', back_populates='customers')