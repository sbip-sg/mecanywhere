@echo OFF
echo STARTING PAYMENT SERVICE...

REM Install pip dependencies
venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --port 7002 --reload
