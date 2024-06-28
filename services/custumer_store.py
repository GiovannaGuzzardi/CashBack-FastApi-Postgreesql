from typing import List
from sqlalchemy.orm import Session
from models.custumer_store import CostumerStore
from models.custumer import Custumer
from models.store import Store
from schemes.custumer_store import CustumerStoreCreate


def post_custumer_store(custumer_store: CustumerStoreCreate , db: Session) -> List[dict]:
    # Busca o store pelo id fornecido em custumer_store.id_store
    store = db.query(Store).filter_by(cnpj=custumer_store.cnpj_store).first()
    if not store:
        raise ValueError(f"Não existe uma loja com esse id")
    
    custumer = db.query(Custumer).filter_by(telefone= custumer_store.telefone_client).first()
    if not custumer:
        raise ValueError(f"Não existe um cliente com esse id")
    
    db_custumer_store = CostumerStore(
        id_store=store.id,
        id_custumer=custumer.id
    )


    db.add(db_custumer_store)
    try:
        db.commit()
        db.refresh(db_custumer_store)
    except Exception as e:
        db.rollback()
        raise e
    return db_custumer_store 
