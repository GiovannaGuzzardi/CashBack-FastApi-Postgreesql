from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.database import Base

class CustumerStoreAssociation(Base):
    __tablename__ = 'custumer_store_association'
    
    id_store = Column(UUID(as_uuid=True), ForeignKey('stores.id'), primary_key=True)
    id_custumer = Column(UUID(as_uuid=True), ForeignKey('custumers.id'), primary_key=True)
    account_creation = Column(DateTime, default=datetime.now)
    
# Relationships
    store = relationship("Store", back_populates="custumer_stores")
    custumer = relationship("Custumer", back_populates="custumer_stores")

# relação entre cashback e custumer e store
    
    __table_args__ = (
        PrimaryKeyConstraint('id_store', 'id_custumer'),
        UniqueConstraint('id_store', 'id_custumer'),
    )