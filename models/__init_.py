# models/__init__.py
from .store import Store
from .custumer import Custumer
from .cashback import Cashback
from .sale import Sale
from .custumer_store_association import CustumerStoreAssociation # type: ignore
from sqlalchemy.orm import relationship

# relacionamento entre as tabelas store e custumer muito para muitos
Store.custumer_stores = relationship("CustumerStoreAssociation", back_populates="store")
Custumer.custumer_stores = relationship("CustumerStoreAssociation", back_populates="custumer")

CustumerStoreAssociation.store = relationship("Store", back_populates="custumer_stores")
CustumerStoreAssociation.custumer = relationship("Custumer", back_populates="custumer_stores")

# relacionamento entre as tabelas sale e cashback um para muitos
Sale.cashbacks = relationship("Cashback", back_populates="sale")
Cashback.sale = relationship("Saler", back_populates="cashbacks")

# relacionamento entre as tabelas sale e store e custumer muitos para muitos
Sale.stores = relationship("Store", back_populates="sale")
Sale.custumers = relationship("Custumer", back_populates="sale")
Custumer.sale = relationship("Sale", back_populates="custumers")
Store.sale = relationship("Sale", back_populates="stores")


__all__ = ["Store", "Custumer", "CustumerStoreAssociation", "Cashback", "Sale"]

