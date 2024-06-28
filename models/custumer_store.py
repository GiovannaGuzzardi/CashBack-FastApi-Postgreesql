# from datetime import datetime, timezone
# import uuid
# from sqlalchemy import Column, DateTime, ForeignKey, PrimaryKeyConstraint
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from db.database import Base

# class CostumerStore(Base):
#     __tablename__ = 'costumer_store'
    
#     id_store = Column(UUID(as_uuid=True), ForeignKey('stores.id'), primary_key=True)
#     id_custumer = Column(UUID(as_uuid=True), ForeignKey('custumers.id'), primary_key=True)
#     account_creation = Column(DateTime, default=datetime.now)
    
#     # Relationships
#     store = relationship("Store", back_populates="costumer_stores")
#     custumer = relationship("Custumer", back_populates="costumer_stores")
    
#     __table_args__ = (
#         PrimaryKeyConstraint('id_store', 'id_custumer'),
#     )
