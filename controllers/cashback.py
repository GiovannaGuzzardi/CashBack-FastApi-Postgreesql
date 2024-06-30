
from typing import Annotated
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from db.database import get_db
from models.cashback import Cashback
from schemes.cashback import CashCreate
from schemes.json import http_json
from services.cashback import post_cashback
from sqlalchemy.exc import IntegrityError

router = fastapi.APIRouter()

db_dependency = Annotated[Session,fastapi.Depends(get_db)]

# @router.post("/cashback/", tags=["cashback"])
# async def create_cashback(cashback: CashCreate, db: db_dependency):
#     try:
#         db_cashback = post_cashback(cashback, db)
        
#         return http_json(
#             detail="Cashback Adicionado com sucesso",
#             status_code=201,
#         )
    
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=400,
#             detail= str(e)
#         )
    
@router.put("/cashback/redeem/{id_cash}", tags=["cashback"])
async def redeem_cashback(id_cash: UUID, db: db_dependency):
    try:
        db_store = db.query(Cashback).filter(Cashback.id == id_cash).first()
        if not db_store:
            raise HTTPException(status_code=404, detail="Cashback não encontrado")
        db_store.redeem = True
        
        return http_json(
            detail="Cashback resgatado com sucesso",
            status_code=200,
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail= str(e)
        )