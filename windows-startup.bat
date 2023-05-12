@echo off
REM Prerequisites: Docker ganache container, venv

echo Starting full node...

REM Start Docker container
docker start ganache

REM Wait for container to start up
echo ===========================================================================================
echo Waiting for Docker container to start up...

REM Run Truffle migration command in a separate console
set confirmTruffle=Y
set /p confirmTruffle=Do you need to migrate the smart contracts? (Y/N): (%confirmTruffle%)
if /i "%confirmTruffle%"=="Y" (
  echo ===========================================================================================
  echo Starting truffle migration...
  echo ===========================================================================================
  cd full_node/contract
  @REM npm ci --prefer-offline --no-audit
  call truffle migrate --network development
  cd ../..
)

REM Start python application in a separate console
cd full_node/discovery
call venv/Scripts/activate.bat
cd src
start uvicorn main:app --port 7000 --workers 1 --reload

pause