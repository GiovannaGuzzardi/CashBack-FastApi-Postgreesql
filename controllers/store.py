import uuid
import fastapi
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from db.database import get_db
from sqlalchemy.orm import Session
from models.store import Store
from schemes.store import StoreBase, StoreCreate
from services.store import post_store
from schemes.json import http_json
from sqlalchemy.exc import IntegrityError

router = fastapi.APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]


@router.post("/stores/", response_model=http_json)
async def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    try:
        db_store = post_store(store, db)
        
        return http_json(
            detail="Loja Adicionada com sucesso",
            status_code=201,
        )

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Erro ao adicionar a loja. Já existe uma loja com este CNPJ ou Email.",
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail= str(e)
        )
   