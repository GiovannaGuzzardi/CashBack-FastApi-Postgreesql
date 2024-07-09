from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime,timezone
import pytz

from schemes.cashback import CashCreate

timezone_brasilia = pytz.timezone('America/Sao_Paulo')

class SaleBase(BaseModel):
    id_sale : UUID
    id_customer : UUID
    id_store : UUID 
    value : float = Field(default=0.0)
    date_time : datetime = Field(default_factory=lambda: datetime.now(timezone_brasilia))

    @field_validator('value')
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('valor precisa ser positivo')
        return v

class SaleCreate(BaseModel):
    id_customer : UUID
    id_store : UUID 
    value : float = Field(default=0.0)

    @field_validator('value')
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('valor precisa ser positivo')
        return v

# Tabela venda (Venda):
# id_venda (Chave Primária)
# cliente_comprador (Chave Estrangeira referenciando cliente.id_cliente)
# loja_vendedora (Chave Estrangeira referenciando loja.id_loja)
# valor
# data_hora
# id_cash (Chave Estrangeira referenciando cash.id_cash)