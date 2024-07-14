from typing import Annotated
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.cashback import Cashback
from models.customer import Customer
from models.customer_store_association import CustomerStoreAssociation
from models.sale import Sale
from models.store import Store
from schemes.json import http_json
from schemes.sale import SaleCreate
from schemes.cashback import percent_cash
from sqlalchemy.exc import IntegrityError


router = fastapi.APIRouter(
    prefix="/sale",
    tags=["sale"]
)

db_dependency = Annotated[Session,Depends(get_db)]

@router.post ("/")
async def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        # conferir se cliente e loja existem
        store = db.query(Store).filter(Store.id == sale.id_store).first()
        customer = db.query(Customer).filter(Customer.id == sale.id_customer).first()
        if not store or not customer:
            raise HTTPException(status_code=404, detail="Loja ou Cliente não encontrados!")
        # conferir se associação existe
        association = db.query(CustomerStoreAssociation).filter(
            CustomerStoreAssociation.id_store == sale.id_store,
            CustomerStoreAssociation.id_customer == sale.id_customer
        ).first()
        if not association:
            # criar a associação
            new_association = CustomerStoreAssociation(
                id_store=sale.id_store,
                id_customer=sale.id_customer,
            )
            db.add(new_association)
            db.commit()
            db.refresh(new_association)
        # Adicionar a venda
        new_sale = Sale(
            id_customer=sale.id_customer,
            id_store=sale.id_store,
            value=sale.value,
        )

        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)

        # Adicionar o cashback

        new_cashback = Cashback(
            id_sale=new_sale.id,
            value= new_sale.value * percent_cash / 100,
            percent= percent_cash,
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