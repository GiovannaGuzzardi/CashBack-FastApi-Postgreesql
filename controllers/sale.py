from typing import Annotated
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.cashback import Cashback
from models.custumer import Custumer
from models.custumer_store_association import CustumerStoreAssociation
from models.sale import Sale
from models.store import Store
from schemes.json import http_json
from schemes.sale import SaleCreate
from schemes.cashback import percent_cash
from sqlalchemy.exc import IntegrityError


router = fastapi.APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]

@router.post ("/sale/", tags=["sales"])
async def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        # conferir se cliente e loja existem
        store = db.query(Store).filter(Store.id == sale.id_store).first()
        custumer = db.query(Custumer).filter(Custumer.id == sale.id_custumer).first()
        if not store or not custumer:
            raise HTTPException(status_code=404, detail="Loja ou Cliente não encontrados!")
        # conferir se associação existe
        association = db.query(CustumerStoreAssociation).filter(
            CustumerStoreAssociation.id_store == sale.id_store,
            CustumerStoreAssociation.id_custumer == sale.id_custumer
        ).first()
        if not association:
            # criar a associação
            new_association = CustumerStoreAssociation(
                id_store=sale.id_store,
                id_custumer=sale.id_custumer,
            )
            db.add(new_association)
            db.commit()
            db.refresh(new_association)
        # Adicionar a venda
        new_sale = Sale(
            id_custumer=sale.id_custumer,
            id_store=sale.id_store,
            value=sale.value,
            date_time=sale.date_time,
        )

        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)

        # Adicionar o cashback

        new_cashback = Cashback(
            id_sale=new_sale.id,
            value= new_sale.value * percent_cash / 100,
            percentage= percent_cash,
        )

        db.add(new_cashback)
        db.commit()
        db.refresh(new_cashback)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Erro ao adicionar a venda.",
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail= str(e)
        )

    return http_json(
            detail="Venda Adicionada com sucesso",
            status_code=201,
    )