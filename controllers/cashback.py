
from typing import Annotated, List
import uuid
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from db.database import get_db
from models.cashback import Cashback
from schemes.cashback import CashCreate,CashBase
from models.sale import Sale
from schemes.json import http_json
from services.cashback import post_cashback
from sqlalchemy.exc import IntegrityError

router = fastapi.APIRouter()

db_dependency = Annotated[Session,fastapi.Depends(get_db)]

# # @router.post("/cashback/", tags=["cashback"])
# # async def create_cashback(cashback: CashCreate, db: db_dependency):
# #     try:
# #         db_cashback = post_cashback(cashback, db)
        
# #         return http_json(
# #             detail="Cashback Adicionado com sucesso",
# #             status_code=201,
# #         )
    
# #     except Exception as e:
# #         db.rollback()
# #         raise HTTPException(
# #             status_code=400,
# #             detail= str(e)
# #         )
    

@router.put("/cashback/redeem/{id_cash}", tags=["cashback"])
async def redeem_cashback(id_cash: uuid.UUID, db: db_dependency):
    try:
        db_store = db.query(Cashback).filter(Cashback.id == id_cash).first()
        if not db_store:
            raise HTTPException(status_code=404, detail="Cashback não encontrado")
        
        if db_store.redeem == True:
            raise HTTPException(status_code=400, detail="Cashback já resgatado")

        db_store.redeem = True
        db.commit()  # Comitar a transação
        
        return http_json(
            detail="Cashback resgatado com sucesso",
            status_code=200,  # Ajustado para 'status' em vez de 'status_code'
            data=None,
            error=None
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/cashcabk/{id_store}/{id_customer}/", tags=["cashback"])
def get_cashback(id_store: str, id_customer: str, db: db_dependency):
    try:
        # Encontrar as vendas associadas ao cliente e à loja selecionados
        db_sale = db.query(Sale).filter(Sale.id_store == id_store, Sale.id_customer == id_customer).all()

        if not db_sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        # Encontrar cashback associado às vendas
        cashbacks = []

        for sale in db_sale:
            db_cashback = db.query(Cashback).filter(Cashback.id_sale == sale.id).all()
            cashbacks.extend(db_cashback)

        if not cashbacks:
            raise HTTPException(status_code=404, detail="Cashback não encontrado")        

        cashbacks_redeen = [cashback for cashback in cashbacks if cashback.redeem ==  True]
        total_cashback_value = sum(cashback.value for cashback in cashbacks_redeen)

        return {
            "cashback": cashbacks_redeen,
            "total": total_cashback_value
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.put("/cashcabk/{id_store}/{id_customer}/redeem", tags=["cashback"])
def redeem_cashback(id_store: str, id_customer: str, db: db_dependency):
    try:
        # Encontrar as vendas associadas ao cliente e à loja selecionados
        db_sale = db.query(Sale).filter(Sale.id_store == id_store, Sale.id_customer == id_customer).all()

        if not db_sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        # Encontrar cashback associado às vendas
        cashbacks = []

        for sale in db_sale:
            db_cashback = db.query(Cashback).filter(Cashback.id_sale == sale.id).all()
            cashbacks.extend(db_cashback)

        if not cashbacks:
            raise HTTPException(status_code=404, detail="Cashback não encontrado")        

        cashbacks_redeen = [cashback for cashback in cashbacks if cashback.redeem ==  False]

        if not cashbacks_redeen:
            raise HTTPException(status_code=400, detail="Nenhum cashback disponível para resgate")

        for cashback in cashbacks_redeen:
            cashback.redeem = True

        db.commit()  # Comitar a transação

        return http_json(
            detail="Cashback resgatado com sucesso",
            status_code=200,  # Ajustado para 'status' em vez de 'status_code'
            data=None,
            error=None
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# cadastrar cliente -  ok 
# cadastrar venda - ok 
# resgate total 
# mostrar valor de cash total 

