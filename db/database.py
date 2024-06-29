from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
import os

URL_DATABASE = 'postgresql://postgres:nova_senha@localhost:5432/cash_database'

engine = create_engine(URL_DATABASE , connect_args={} , future=True)

SessionLocal = sessionmaker(autocommit= False , autoflush= False, bind=engine, future = True)

Base = declarative_base()

# modelo de dados, criei o arquivo database.py(pre requisito de models) e models.py
# agora vou criar a conexão com o bd
def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()