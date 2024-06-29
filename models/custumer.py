import uuid
from sqlalchemy import UUID, Boolean,Column, ForeignKey, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class Custumer(Base):
    __tablename__ = 'custumers'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    cpf= Column(String, index=True, unique= True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, nullable=True)
    telefone = Column(String, unique =True)

     # Relacionamento muitos para muitos com a tabela Store
    # stores = relationship("Store", secondary="custumer_store", back_populates="custumers", uselist=True)

    # stores = relationship("Store", back_populates="custumers", uselist=True)