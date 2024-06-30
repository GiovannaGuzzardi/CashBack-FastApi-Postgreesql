from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID

class CashBase(BaseModel):
    id: UUID
    redeem : bool = Field(default=False)
    value: float = Field(default=0.0)
    percent: float = Field(default=0.0)
    id_sale: UUID

    @field_validator('value', 'percent')
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('Must be positive')
        return v


class CashCreate(BaseModel):
    redeem: bool = Field(default=False)
    value: float = Field(default=0.0)
    percent: float = Field(default=10)
    id_sale: UUID


    @field_validator('value' , 'percent')
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('O valor do cash deve ser positivo ou negativo')
        return v

percent_cash = 10
