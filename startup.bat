@echo off

REM Start Docker container
docker start ganache

REM Start rabbitmq
echo Ensure your rabbitmq server is started

REM Install contract dependencies
set confirmContract=Y
set /p confirmContract=Do you need to install contract dependencies? (Y/N): (%confirmContract%)
if /i "%confirmContract%"=="Y" (
    echo ===========================================================================================
    echo Installing contract dependencies...
    echo ===========================================================================================
    cd did\contract
    call npm ci --prefer-offline --no-audit
    cd ..\..

    cd full_node\contract
    call npm ci --prefer-offline --no-audit
    cd ..\..
)


REM Run Truffle migration command in a separate console
set confirmTruffle=Y
set /p confirmTruffle=Do you need to migrate the smart contracts? (Y/N): (%confirmTruffle%)
if /i "%confirmTruffle%"=="Y" (
    echo ===========================================================================================
    echo Starting truffle migration...
    echo ===========================================================================================
    cd did\contract
    call truffle migrate --network development
    cd ..\..

    cd full_node\contract
    call truffle migrate --network development
    cd ..\..
)


cd did
call did-local-startup.bat
cd ..
start "issuer" cmd.exe /k "cd authentication && auth-startup.bat"
start "fullnode" cmd.exe /k "cd full_node && fullnode-startup.bat"
