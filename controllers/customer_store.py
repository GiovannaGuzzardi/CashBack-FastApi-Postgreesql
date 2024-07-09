from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy.orm import Session
from db.database import get_db
from models.customer import customer
from models.customer_store_association import customerStoreAssociation
from models.store import Store
from schemes.customer_store import customerStoreBase, customerStoreCreate 
from schemes.json import http_json
# from services.customer_store import 
from sqlalchemy.exc import IntegrityError

from services.customer_store import post_customer_store


router = fastapi.APIRouter()
db_dependency = Annotated[Session,fastapi.Depends(get_db)]

@router.post("/customer_store_association/", tags=["customer_store"])
async def create_customer_store_association(association: customerStoreCreate, db: Session = Depends(get_db)):
    try:
        new_association = post_customer_store( association, db)
        return new_association
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Associação já existente!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/store_association/store/{id}", tags=["customer_store"])
async def get_store_association(id: UUID, db: Session = Depends(get_db)):
    try:
        store = db.query(Store).filter(Store.id == id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada!")
        store_association = db.query(customerStoreAssociation).filter(customerStoreAssociation.id_store == id).all()
        return store_association
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/store_association/customer/{id}", tags=["customer_store"])
async def get_customer_association(id: UUID, db: Session = Depends(get_db)):
    try:
        customer = db.query(customer).filter(customer.id == id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Cliente não encontrado!")
        customer_association = db.query(customerStoreAssociation).filter(customerStoreAssociation.id_customer == id).all()
        return customer_association
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
