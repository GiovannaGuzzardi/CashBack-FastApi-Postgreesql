from typing import List
from sqlalchemy.orm import Session

from models.store import Store
from schemes.store import StoreCreate


def post_store(store: StoreCreate, db: Session) -> List[dict]:
    db_store = Store(cnpj=store.cnpj, name=store.name, email=store.email)
    db.add(db_store)
    try:
        db.commit()
        db.refresh(db_store)
    except Exception as e:
        db.rollback()
        raise e
    return db_store
