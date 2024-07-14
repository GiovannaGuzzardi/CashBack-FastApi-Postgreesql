from datetime import datetime, timezone
from pydantic import BaseModel,Field
from uuid import UUID
import pytz

timezone_brasilia = pytz.timezone('America/Sao_Paulo')

class CustomerStoreBase(BaseModel):
    id_store : UUID
    id_customer : UUID
    account_creation: datetime = Field(default_factory=lambda: datetime.now(timezone_brasilia))

class CustomerStoreCreate(BaseModel):
    id_store : UUID
    id_customer : UUID

