from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.customer_store_association import CustomerStoreAssociation
from models.customer import Customer
from models.store import Store
from schemes.customer_store import CustomerStoreCreate


def post_customer_store(association: CustomerStoreCreate , db: Session) -> List[dict]:
    store = db.query(Store).filter(Store.id == association.id_store).first()
    customer = db.query(Customer).filter(Customer.id == association.id_customer).first()
    if not store or not customer:
        raise HTTPException(status_code=404, detail="Loja ou Cliente não encontrados!")
    # Criar a associação
    new_association = CustomerStoreAssociation(
        id_store=association.id_store,
        id_customer=association.id_customer,
    )
    db.add(new_association)
    db.commit()
    db.refresh(new_association)
    return new_association