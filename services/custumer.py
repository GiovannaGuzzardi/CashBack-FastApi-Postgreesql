from typing import List
from sqlalchemy.orm import Session

from models.custumer import Custumer
from schemes.custumer import CustumerCreate


def post_custumer(custumer: CustumerCreate, db: Session) -> List[dict]:
    db_custumer = Custumer(name=custumer.name, cpf=custumer.cpf, email=custumer.email, telefone=custumer.telefone)
    db.add(db_custumer)
    try:
        db.commit()
        db.refresh(db_custumer)
    except Exception as e:
        db.rollback()
        raise e
    return db_custumer

def list_custumer(db: Session) -> List[dict]:
    db_custumer = db.query(Custumer).all()
    if not db_custumer:
        raise Exception("Não tem nenhum cliente aqui!")
    return db_custumer

def get_custumer_by_id(custumer_id: str, db: Session) -> List[dict]:
    db_custumer = db.query(Custumer).filter(Custumer.id == custumer_id).first()
    if not db_custumer:
        raise Exception("Não tem nenhum cliente com esse id")
    return db_custumer

def get_custumer_by_cpf(cpf: str, db: Session) -> List[dict]:
    db_custumer = db.query(Custumer).filter(Custumer.cpf == cpf).first()
    if not db_custumer:
        raise Exception("Não tem nenhum cliente com esse cpf")
    return db_custumer

def get_custumer_by_phone(phone: str, db: Session) -> List[dict]:
    db_custumer = db.query(Custumer).filter(Custumer.telefone == phone).first()
    if not db_custumer:
        raise Exception("Não tem nenhum cliente com esse telefone")
    return db_custumer

def get_custumer_by_email(email: str, db: Session) -> List[dict]:
    db_custumer = db.query(Custumer).filter(Custumer.email == email).first()
    if not db_custumer:
        raise Exception("Não tem nenhum cliente com esse e-mail")
    return db_custumer

def delete_custumer_service(custumer_id: str, db: Session) -> List[dict]:
    db_custumer = db.query(Custumer).filter(Custumer.id == custumer_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return db_custumer

def update_custumer_service(custumer_id: str, custumer: CustumerCreate, db: Session) -> List[dict]:
    db_custumer = db.query(Custumer).filter(Custumer.id == custumer_id).first()
    if not db_custumer:
        raise Exception("Não tem nenhum cliente com esse id")
    db_custumer.cnpj = custumer.cnpj
    db_custumer.name = custumer.name
    db_custumer.email = custumer.email
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return db_custumer