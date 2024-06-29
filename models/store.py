import uuid
from sqlalchemy import UUID, Boolean,Column, ForeignKey, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class Store(Base):
    __tablename__ = 'stores'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    cnpj = Column(String, unique=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)                         

    custumer_stores = relationship("CustumerStoreAssociation", back_populates="store")