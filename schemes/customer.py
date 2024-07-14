from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class CustomerBase(BaseModel):
    id : UUID
    cpf: str = Field(min_length=11 , max_length=11)
    name: str = Field(min_length=1 , max_length=50)
    email: EmailStr  
    telefone : str = Field(min_length=1 , max_length=15)

class CustomerCreate(BaseModel):
    cpf: str = Field(min_length=11 , max_length=11)
    name: str = Field(min_length=1 , max_length=50)
    email: EmailStr  
    telefone : str = Field(min_length=1 , max_length=15)


# Tabela cliente (Cliente):
# id_cliente (Chave Primária)
# cpf (Chave Única)
# nome
# e-mail (Chave Única)
# telefone(chave Única)