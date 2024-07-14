import uuid
import fastapi
from typing import Annotated, List
from fastapi import Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from db.database import get_db
from sqlalchemy.orm import Session
from models.store import Store
from schemes.store import StoreBase, StoreCreate
from services.store import delete_store_service, get_store_by_cnpj, get_store_by_email, get_store_by_id, list_store, post_store, update_store_service
from schemes.json import http_json
from sqlalchemy.exc import IntegrityError

router = fastapi.APIRouter(
    prefix="/store",
    tags=["store"]
)

db_dependency = Annotated[Session,Depends(get_db)]

@router.post("/", response_model=http_json)
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

@router.get("/", response_model= List[StoreBase])
async def read_stores(db: db_dependency):
    try:
        result = list_store(db)
        if not result:
            raise HTTPException(status_code=404 , detail= "Não tem nenhuma loja aqui" )
    except Exception as e:
        raise HTTPException(status_code=400 , detail= str(e) )
    return result

@router.get("/{store_id}", response_model=StoreBase)
async def read_store(store_id: uuid.UUID, db: db_dependency, ):
    try:
        result = get_store_by_id(store_id, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.get("/cnpj/{cnpj}/", response_model=StoreBase )
async def read_question(cnpj: str, db: db_dependency):
    try:
        result = get_store_by_cnpj(cnpj, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.get("/email/{email}", response_model=StoreBase)
async def read_question(email: str, db: db_dependency):
    try:
        result = get_store_by_email(email, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.delete("/{store_id}", response_model=http_json)
async def delete_store(store_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        delete_store_service(store_id, db)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail= str(e)
        )
    return http_json(
            detail="Loja deletada com sucesso",
            status_code=200,
        )

@router.put("/{store_id}", response_model=http_json)
async def update_store(store_id: uuid.UUID, store: StoreCreate, db: Session = Depends(get_db)):
    try:
        update_store_service(store_id, store, db)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail= str(e)
        )
    return http_json(
            detail="Loja atualizada com sucesso",
            status_code=200,
        )

# Crud completo , service e controller separados
