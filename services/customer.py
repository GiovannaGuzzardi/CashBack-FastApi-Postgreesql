from typing import List
from sqlalchemy.orm import Session

from models.customer import customer
from schemes.customer import customerCreate


def post_customer(customer: customerCreate, db: Session) -> List[dict]:
    db_customer = customer(name=customer.name, cpf=customer.cpf, email=customer.email, telefone=customer.telefone)
    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
    except Exception as e:
        db.rollback()
        raise e
    return db_customer

def list_customer(db: Session) -> List[dict]:
    db_customer = db.query(customer).all()
    if not db_customer:
        raise Exception("Não tem nenhum cliente aqui!")
    return db_customer

def get_customer_by_id(customer_id: str, db: Session) -> List[dict]:
    db_customer = db.query(customer).filter(customer.id == customer_id).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse id")
    return db_customer

def get_customer_by_cpf(cpf: str, db: Session) -> List[dict]:
    db_customer = db.query(customer).filter(customer.cpf == cpf).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse cpf")
    return db_customer

def get_customer_by_phone(phone: str, db: Session) -> List[dict]:
    db_customer = db.query(customer).filter(customer.telefone == phone).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse telefone")
    return db_customer

def get_customer_by_email(email: str, db: Session) -> List[dict]:
    db_customer = db.query(customer).filter(customer.email == email).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse e-mail")
    return db_customer

def delete_customer_service(customer_id: str, db: Session) -> List[dict]:
    db_customer = db.query(customer).filter(customer.id == customer_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return db_customer

def update_customer_service(customer_id: str, customer: customerCreate, db: Session) -> List[dict]:
    db_customer = db.query(customer).filter(customer.id == customer_id).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse id")
    db_customer.cnpj = customer.cnpj
    db_customer.name = customer.name
    db_customer.email = customer.email
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return db_customer