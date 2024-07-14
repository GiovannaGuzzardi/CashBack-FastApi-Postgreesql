from typing import List
from sqlalchemy.orm import Session

from models.customer import Customer
from schemes.customer import CustomerCreate



def post_customer(customer: CustomerCreate, db: Session) -> List[dict]:
    db_customer = Customer(name=customer.name, cpf=customer.cpf, email=customer.email, telefone=customer.telefone)
    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
    except Exception as e:
        db.rollback()
        raise e
    return db_customer

def list_customer(db: Session) -> List[dict]:
    db_customer = db.query(Customer).all()
    if not db_customer:
        raise Exception("Não tem nenhum cliente aqui!")
    return db_customer

def get_customer_by_id(customer_id: str, db: Session) -> List[dict]:
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse id")
    return db_customer

def get_customer_by_cpf(cpf: str, db: Session) -> List[dict]:
    db_customer = db.query(Customer).filter(Customer.cpf == cpf).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse cpf")
    return db_customer

def get_customer_by_phone(phone: str, db: Session) -> List[dict]:
    db_customer = db.query(Customer).filter(Customer.telefone == phone).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse telefone")
    return db_customer

def get_customer_by_email(email: str, db: Session) -> List[dict]:
    db_customer = db.query(Customer).filter(Customer.email == email).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse e-mail")
    return db_customer

def delete_customer_service(customer_id: str, db: Session) -> List[dict]:
    db_customer = db.query(Customer).filter(Customer.id == customer_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return db_customer

def update_customer_service(customer_id: str, customer: CustomerCreate, db: Session) -> List[dict]:
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise Exception("Não tem nenhum cliente com esse id")
    db_customer.cpf = customer.cpf
    db_customer.name = customer.name
    db_customer.email = customer.email
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return db_customer