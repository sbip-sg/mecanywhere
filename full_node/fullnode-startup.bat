@echo off
REM Prerequisites: Docker ganache container, venv

echo STARTING FULL NODE...

REM Start rabbitmq docker container
docker start amqp.test
REM Start redis docker container
docker start redis

REM Start python application in a separate console
start "discovery" cmd.exe /k "cd discovery && venv\Scripts\activate && pip install -r requirements.txt && cd src && uvicorn main:app --port 7000 --reload"

REM Start python application in a separate console
start "transaction" cmd.exe /k "cd transaction && venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --port 7001 --reload"
