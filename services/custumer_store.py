from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.custumer_store_association import CustumerStoreAssociation
from models.custumer import Custumer
from models.store import Store
from schemes.custumer_store import CustumerStoreCreate


def post_custumer_store(association: CustumerStoreCreate , db: Session) -> List[dict]:
    store = db.query(Store).filter(Store.id == association.id_store).first()
    custumer = db.query(Custumer).filter(Custumer.id == association.id_custumer).first()
    if not store or not custumer:
        raise HTTPException(status_code=404, detail="Loja ou Cliente não encontrados!")
    # Criar a associação
    new_association = CustumerStoreAssociation(
        id_store=association.id_store,
        id_custumer=association.id_custumer,
    )
    db.add(new_association)
    db.commit()
    db.refresh(new_association)
    return new_association