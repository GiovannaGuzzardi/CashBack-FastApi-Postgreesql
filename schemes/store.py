from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class StoreBase(BaseModel):
    id : UUID
    cnpj: str = Field(min_length=14 , max_length=14)
    name: str
    email: EmailStr   
    active: bool = Field(default=True)
    password: str

class StoreCreate(BaseModel):
    cnpj: str = Field(min_length=14, max_length=14)
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=50)


# Tabela loja (Loja):
# id_loja (Chave Primária)
# cnpj (Chave Única)
# nome
# e-mail (Chave Única)