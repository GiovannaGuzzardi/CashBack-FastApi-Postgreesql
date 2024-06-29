from services.custumer import delete_custumer_service, get_custumer_by_cpf, get_custumer_by_email, get_custumer_by_id, get_custumer_by_phone, list_custumer, post_custumer, update_custumer_service
from typing import Annotated, List
import uuid
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy.orm import Session
from db.database import get_db
from schemes.custumer import CustumerBase, CustumerCreate
from schemes.json import http_json
from sqlalchemy.exc import IntegrityError


router = fastapi.APIRouter()

db_dependency = Annotated[Session,fastapi.Depends(get_db)]

@router.post("/custumers/", tags=["custumers"])
async def create_custumer(custumer: CustumerCreate, db: Session = Depends(get_db)):
    try:
        db_custumer = post_custumer(custumer, db)
        
        return http_json(
            detail="Cliente Adicionado com sucesso",
            status_code=201,
        )

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Erro ao adicionar o cliente. Já existe um cliente com este CPF ou Email.",
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail= str(e)
        )
    
@router.get("/custumers/", response_model= List[CustumerBase] ,tags=["custumers"])
async def read_custumers(db: db_dependency):
    try:
        result = list_custumer(db)
        if not result:
            raise HTTPException(status_code=404 , detail= "Não tem nenhum cliente aqui" )
    except Exception as e:
        raise HTTPException(status_code=400 , detail= str(e) )
    return result

@router.get("/custumer/{custumer_id}", response_model=CustumerBase ,tags=["custumers"])
async def read_custumer_id(custumer_id: uuid.UUID, db: db_dependency):
    try:
        result = get_custumer_by_id(custumer_id, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.get("/custumer/cpf/{cpf}/", response_model=CustumerBase ,tags=["custumers"])
async def read_custumer_cpf(cpf: str, db: db_dependency):
    try:
        result = get_custumer_by_cpf(cpf, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.get("/custumer/phone/{phone}/", response_model=CustumerBase ,tags=["custumers"])
async def read_custumer_phone(phone: str, db: db_dependency):
    try:
        result = get_custumer_by_phone(phone, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.get("/custumer/email/{email}", response_model=CustumerBase ,tags=["custumers"])
async def read_custumer_email(email: str, db: db_dependency):
    try:
        result = get_custumer_by_email(email, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.delete("/custumer/{custumer_id}", response_model=http_json ,tags=["custumers"])
async def delete_custumer(custumer_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        delete_custumer_service(custumer_id, db)
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

@router.put("/custumer/{custumer_id}", response_model=http_json ,tags=["custumers"])
async def update_custumer(custumer_id: uuid.UUID, custumer: CustumerCreate, db: Session = Depends(get_db)):
    try:
        update_custumer_service(custumer_id, custumer, db)
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