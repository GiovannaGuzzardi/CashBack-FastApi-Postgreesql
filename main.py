from datetime import datetime
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import controllers.store as api_store
from db.database import engine, get_db
import models
import models.store
from fastapi.exceptions import RequestValidationError
import controllers.customer as api_customer
import controllers.cashback as api_cashback
import controllers.customer_store as api_customer_store
import controllers.sale as api_sale
import controllers.auth as api_auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cyrus Cash",
    description="api para gerar cashback de vendas",
    version="0.0.1",
    contact={
        "name": "cyrus",
        "email": "cyrus.tech909@gmail.com"
    },
    license_info={
        "name":"MIT"
    }
)

# Adiciona o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (para ambiente de desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = "Erro de validação: campos obrigatórios faltando."
    return JSONResponse(
        status_code=422,
        content={"msg": error_msg, "detail": exc.errors()}
    )



models.store.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(api_auth.get_current_user)]

@app.get("/" , status_code=status.HTTP_200_OK)
async def user(user: user_dependency , db : db_dependency):
    if not user:
        raise HTTPException(status_code=401 , detail="Usuário não autenticado")        
    return {"store" : user}

app.include_router(api_store.router)
app.include_router(api_customer.router)
app.include_router(api_cashback.router)
app.include_router(api_customer_store.router)
app.include_router(api_sale.router)
app.include_router(api_auth.router) 