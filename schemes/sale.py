from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime,timezone

def get_utc_now():
    return datetime.now(timezone.utc)

class SaleBase(BaseModel):
    id_sale : UUID
    custumer_buyer : UUID
    seller_store : UUID 
    value : float = Field(default=0.0)
    data_hora : datetime =   Field(default_factory=get_utc_now())
    porcent_cash : float=  Field(default=10.0)
    cash_generated : UUID

    class Config:
        orm_mode = True

    @field_validator('value', 'percentage_cash')
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('Must be positive')
        return v


# Tabela venda (Venda):
# id_venda (Chave Primária)
# cliente_comprador (Chave Estrangeira referenciando cliente.id_cliente)
# loja_vendedora (Chave Estrangeira referenciando loja.id_loja)
# valor
# data_hora
# id_cash (Chave Estrangeira referenciando cash.id_cash)