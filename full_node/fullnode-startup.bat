@echo off
REM Prerequisites: Docker ganache container, venv

echo STARTING FULL NODE...

REM Start rabbitmq docker container
docker start amqp.test
REM Start redis docker container
docker start redis

REM Start python application in a separate console
cd discovery

REM Install pip dependencies
venv\Scripts\activate && pip install -r requirements.txt && cd src && uvicorn main:app --port 7000 --workers 1 --reload

