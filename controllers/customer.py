from services.customer import delete_customer_service, get_customer_by_cpf, get_customer_by_email, get_customer_by_id, get_customer_by_phone, list_customer, post_customer, update_customer_service
from typing import Annotated, List
import uuid
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy.orm import Session
from db.database import get_db
from schemes.customer import CustomerBase, CustomerCreate
from schemes.json import http_json
from sqlalchemy.exc import IntegrityError


router = fastapi.APIRouter()

db_dependency = Annotated[Session,fastapi.Depends(get_db)]

@router.post("/customers/", tags=["customers"])
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        db_customer = post_customer(customer, db)
        
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
    
@router.get("/customers/", response_model= List[CustomerBase] ,tags=["customers"])
async def read_customers(db: db_dependency):
    try:
        result = list_customer(db)
        if not result:
            raise HTTPException(status_code=404 , detail= "Não tem nenhum cliente aqui" )
    except Exception as e:
        raise HTTPException(status_code=400 , detail= str(e) )
    return result

@router.get("/customer/{customer_id}", response_model=CustomerBase ,tags=["customers"])
async def read_customer_id(customer_id: uuid.UUID, db: db_dependency):
    try:
        result = get_customer_by_id(customer_id, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.get("/customer/cpf/{cpf}/", response_model=CustomerBase ,tags=["customers"])
async def read_customer_cpf(cpf: str, db: db_dependency):
    try:
        result = get_customer_by_cpf(cpf, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.get("/customer/phone/{phone}/", response_model=CustomerBase ,tags=["customers"])
async def read_customer_phone(phone: str, db: db_dependency):
    try:
        result = get_customer_by_phone(phone, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.get("/customer/email/{email}", response_model=CustomerBase ,tags=["customers"])
async def read_customer_email(email: str, db: db_dependency):
    try:
        result = get_customer_by_email(email, db)
    except Exception as e:
        raise HTTPException(status_code=404 , detail= str(e) )
    return result

@router.delete("/customer/{customer_id}", response_model=http_json ,tags=["customers"])
async def delete_customer(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        delete_customer_service(customer_id, db)
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

@router.put("/customer/{customer_id}", response_model=http_json ,tags=["customers"])
async def update_customer(customer_id: uuid.UUID, customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        update_customer_service(customer_id, customer, db)
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