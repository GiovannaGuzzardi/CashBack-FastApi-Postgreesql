## Getting Started

    First, run the localhost api:

    ```bash
    #### activate scritp:
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    #### create env:
        ctrl + shift + p 
        create environment ou criar variavel de ambiente   
    #### add dependencies in requirements
    #### activate venv    
        .\.venv\Scripts\activate 
    #### case need upgrade requirements.txt
        pip freeze > requirements.txt
    #### alembic upgrade head
        adicionar pass na ultima version alembic
        alembic revision --autogenerate -m "bora ver se funciona"
    #### run the localhost api:
        uvicorn main:app --reload - roda ai moleque
    