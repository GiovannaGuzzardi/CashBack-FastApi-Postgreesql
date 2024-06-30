from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import controllers.store as api_store
from db.database import engine
import models
import models.store
from fastapi.exceptions import RequestValidationError
import controllers.custumer as api_custumer
import controllers.cashback as api_cashback
import controllers.custumer_store as api_custumer_store
import controllers.sale as api_sale

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = "Erro de validação: campos obrigatórios faltando."
    return JSONResponse(
        status_code=422,
        content={"msg": error_msg, "detail": exc.errors()}
    )



models.store.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_store.router)
app.include_router(api_custumer.router)
app.include_router(api_cashback.router)
app.include_router(api_custumer_store.router)
app.include_router(api_sale.router)
