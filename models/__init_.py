# models/__init__.py
from .store import Store
from .customer import customer
from .cashback import Cashback
from .sale import Sale
from .customer_store_association import customerStoreAssociation # type: ignore
from sqlalchemy.orm import relationship

# relacionamento entre as tabelas store e customer muito para muitos
Store.customer_stores = relationship("customerStoreAssociation", back_populates="store")
customer.customer_stores = relationship("customerStoreAssociation", back_populates="customer")

customerStoreAssociation.store = relationship("Store", back_populates="customer_stores")
customerStoreAssociation.customer = relationship("customer", back_populates="customer_stores")

# relacionamento entre as tabelas sale e cashback um para muitos
Sale.cashbacks = relationship("Cashback", back_populates="sale")
Cashback.sale = relationship("Saler", back_populates="cashbacks")

# relacionamento entre as tabelas sale e store e customer muitos para muitos
Sale.stores = relationship("Store", back_populates="sale")
Sale.customers = relationship("customer", back_populates="sale")
customer.sale = relationship("Sale", back_populates="customers")
Store.sale = relationship("Sale", back_populates="stores")


__all__ = ["Store", "customer", "customerStoreAssociation", "Cashback", "Sale"]

