# models/__init__.py
from .store import Store
from .custumer import Custumer
from .custumer_store_association import CustumerStoreAssociation # type: ignore
from sqlalchemy.orm import relationship

# Definir relacionamentos depois que todas as classes foram importadas
Store.custumer_stores = relationship("CustumerStoreAssociation", back_populates="store")
Custumer.custumer_stores = relationship("CustumerStoreAssociation", back_populates="custumer")

CustumerStoreAssociation.store = relationship("Store", back_populates="custumer_stores")
CustumerStoreAssociation.custumer = relationship("Custumer", back_populates="custumer_stores")

__all__ = ["Store", "Custumer", "CustumerStoreAssociation"]

# 9247d7f1-7508-44be-85e5-028d2b1c443a
# dbd55143-68f7-4bc7-b320-e3dccb611f55