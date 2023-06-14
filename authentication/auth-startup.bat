@echo OFF
echo STARTING PO AUTHENTICATION SERVICE...

REM Install pip dependencies
venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --port 8000 --workers 1 --reload
