from typing import List
from sqlalchemy.orm import Session

from models.cashback import Cashback
from schemes.cashback import CashCreate


def post_cashback(cashback: CashCreate, db: Session) -> List[dict]:
    db_cashback = Cashback(redeem=cashback.redeem, value=cashback.value , id_custumer=cashback.id_custumer)
    db.add(db_cashback)
    try:
        db.commit()
        db.refresh(db_cashback)
    except Exception as e:
        db.rollback()
        raise e
    return db_cashback

