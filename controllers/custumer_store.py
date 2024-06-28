# from typing import Annotated
# from fastapi import Depends, HTTPException
# import fastapi
# from sqlalchemy.orm import Session
# from db.database import get_db
# from schemes.custumer_store import CustumerStoreCreate
# from schemes.json import http_json
# from services.custumer_store import post_custumer_store
# from sqlalchemy.exc import IntegrityError


# router = fastapi.APIRouter()
# db_dependency = Annotated[Session,fastapi.Depends(get_db)]

# @router.post("/sale/stores/custumer/", tags=["sale"])
# async def create_custumer_store(custumer_store: CustumerStoreCreate, db: Session = Depends(get_db)):
#     try:
#         db_custumer_store = post_custumer_store(custumer_store, db)
        
#         return http_json(
#             detail="Relação entre loja e cliente adicionada com sucesso",
#             status_code=201,
#         )

    
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=400,
#             detail= str(e)
#         )
    

#     # except IntegrityError as e:
#     #     db.rollback()
#     #     raise HTTPException(
#     #         status_code=409,
#     #         detail="Erro ao adicionar o cliente. Já existe um cliente com este CPF ou Email.",
#     #     )