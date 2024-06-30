from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy.orm import Session
from db.database import get_db
from models.custumer import Custumer
from models.custumer_store_association import CustumerStoreAssociation
from models.store import Store
from schemes.custumer_store import CustumerStoreBase, CustumerStoreCreate 
from schemes.json import http_json
# from services.custumer_store import 
from sqlalchemy.exc import IntegrityError

from services.custumer_store import post_custumer_store


router = fastapi.APIRouter()
db_dependency = Annotated[Session,fastapi.Depends(get_db)]

@router.post("/custumer_store_association/", tags=["custumer_store"])
async def create_custumer_store_association(association: CustumerStoreCreate, db: Session = Depends(get_db)):
    try:
        new_association = post_custumer_store( association, db)
        return new_association
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Associação já existente!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/store_association/store/{id}", tags=["custumer_store"])
async def get_store_association(id: UUID, db: Session = Depends(get_db)):
    try:
        store = db.query(Store).filter(Store.id == id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada!")
        store_association = db.query(CustumerStoreAssociation).filter(CustumerStoreAssociation.id_store == id).all()
        return store_association
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/store_association/custumer/{id}", tags=["custumer_store"])
async def get_custumer_association(id: UUID, db: Session = Depends(get_db)):
    try:
        custumer = db.query(Custumer).filter(Custumer.id == id).first()
        if not custumer:
            raise HTTPException(status_code=404, detail="Cliente não encontrado!")
        custumer_association = db.query(CustumerStoreAssociation).filter(CustumerStoreAssociation.id_custumer == id).all()
        return custumer_association
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
