from typing import Annotated
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy.orm import Session
from db.database import get_db
from models.custumer import Custumer
from models.custumer_store_association import CustumerStoreAssociation
from models.store import Store
from schemes.custumer_store import CustumerStoreBase 
from schemes.json import http_json
# from services.custumer_store import 
from sqlalchemy.exc import IntegrityError


router = fastapi.APIRouter()
db_dependency = Annotated[Session,fastapi.Depends(get_db)]

@router.post("/custumer_store_association/", tags=["custumer_store"])
async def create_custumer_store_association(association: CustumerStoreBase, db: Session = Depends(get_db)):
    try:
        # Verificar se o Store e o Custumer existem
        store = db.query(Store).filter(Store.id == association.id_store).first()
        custumer = db.query(Custumer).filter(Custumer.id == association.id_custumer).first()
        if not store or not custumer:
            raise HTTPException(status_code=404, detail="Loja ou Cliente não encontrados!")
        
        # Criar a associação
        new_association = CustumerStoreAssociation(
            id_store=association.id_store,
            id_custumer=association.id_custumer,
            account_creation=association.account_creation
        )
        db.add(new_association)
        db.commit()
        db.refresh(new_association)
        return new_association
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))