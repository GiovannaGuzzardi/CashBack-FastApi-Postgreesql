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
