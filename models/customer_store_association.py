from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.database import Base

class customerStoreAssociation(Base):
    __tablename__ = 'customer_store_association'
    
    id_store = Column(UUID(as_uuid=True), ForeignKey('stores.id' , name='fk_association_store'), primary_key=True)
    id_customer = Column(UUID(as_uuid=True), ForeignKey('customers.id' , name='fk_association_customer'), primary_key=True)
    account_creation = Column(DateTime, default=datetime.now)
    
# Relationships
    store = relationship("Store", back_populates="customer_stores")
    customer = relationship("customer", back_populates="customer_stores")

# relação entre cashback e customer e store
    
    __table_args__ = (
        PrimaryKeyConstraint('id_store', 'id_customer'),
        UniqueConstraint('id_store', 'id_customer'),
    )