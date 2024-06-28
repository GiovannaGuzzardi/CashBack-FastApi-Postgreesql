import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float
from db.database import Base


class Cashback(Base):
    __tablename__ = 'cashbacks'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()))
    redeem = Column(Boolean)
    value = Column(Float)


