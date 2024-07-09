from fastapi import APIRouter
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# vai ser usado para gerar o token
SECRET_KEY = 'd1e7b3b3c7b3d7e1'
# vai ser usado para verificar o token
ALGORITHM = 'HS256'

# vai ser usado para criptografar a senha
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str