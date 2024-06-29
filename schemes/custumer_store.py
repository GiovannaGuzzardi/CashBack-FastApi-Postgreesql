from datetime import datetime, timezone
from pydantic import BaseModel,Field
from uuid import UUID
import pytz

timezone_brasilia = pytz.timezone('America/Sao_Paulo')

class CustumerStoreBase(BaseModel):
    id_store : UUID
    id_custumer : UUID
    account_creation: datetime = Field(default_factory=lambda: datetime.now(timezone_brasilia))

class CustumerStoreCreate(BaseModel):
    telefone_client : str
    cnpj_store : str

