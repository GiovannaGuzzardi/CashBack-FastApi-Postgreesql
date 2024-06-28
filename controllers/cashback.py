
from typing import Annotated
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy.orm import Session
from db.database import get_db
from schemes.cashback import CashCreate
from schemes.json import http_json
from services.cashback import post_cashback
from sqlalchemy.exc import IntegrityError

router = fastapi.APIRouter()

db_dependency = Annotated[Session,fastapi.Depends(get_db)]

@router.post("/cashback/", tags=["cashback"])
async def create_cashback(cashback: CashCreate, db: Session = Depends(get_db)):
    try:
        db_cashback = post_cashback(cashback, db)
        
        return http_json(
            detail="Cashback Adicionado com sucesso",
            status_code=201,
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail= str(e)
        )