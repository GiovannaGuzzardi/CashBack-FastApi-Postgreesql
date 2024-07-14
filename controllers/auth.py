from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Form, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated, List
from sqlalchemy.orm import Session
from models.store import Store
from jose import JWTError, jwt

from db.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# vai ser usado para gerar o token
SECRET_KEY = 'd1e7b3b3c7b3d7e1'
# vai ser usado para verificar o token
ALGORITHM = 'HS256'

db_dependency = Annotated[Session,Depends(get_db)]

# vai ser usado para criptografar a senha
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateStoreRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm , Depends()]  , db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
    token = create_access_token(user.email, str(user.id), timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(email: str, password: str, db: db_dependency):
    user = db.query(Store).filter(Store.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(email: str, id: str, expires_delta: timedelta):
    to_encode = {"sub": email, "id": id}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str , Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        user_name: str = payload.get("name")


        if not username  or not user_id :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Este não é um usuario válido"
            )
        return {"email": username, "id": user_id}
    
    except JWTError as e :
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Token inválido : " + str(e),
        )