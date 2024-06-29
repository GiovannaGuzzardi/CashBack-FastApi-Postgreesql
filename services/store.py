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

def list_store(db: Session) -> List[dict]:
    store = db.query(Store).all()
    return store

def get_store_by_id(store_id: str, db: Session) -> List[dict]:
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise Exception("Loja não encontrada")
    return store

def get_store_by_cnpj(cnpj: str, db: Session) -> List[dict]:
    store = db.query(Store).filter(Store.cnpj == cnpj).first()
    if not store:
        raise Exception("Loja não encontrada")
    return store

def get_store_by_email(email: str, db: Session) -> List[dict]:
    store = db.query(Store).filter(Store.email == email).first()
    if not store:
        raise Exception("Loja não encontrada")
    return store

def delete_store_service(store_id: str, db: Session) -> List[dict]:
    store = db.query(Store).filter(Store.id == store_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return store

def update_store_service(store_id: str, store: StoreCreate, db: Session) -> List[dict]:
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise Exception("Loja não encontrada")
    db_store.cnpj = store.cnpj
    db_store.name = store.name
    db_store.email = store.email
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return db_store