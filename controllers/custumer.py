from typing import Annotated
from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy.orm import Session
from db.database import get_db
from schemes.custumer import CustumerCreate
from schemes.json import http_json
from services.custumer import post_custumer
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