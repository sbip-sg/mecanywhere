@echo off
REM Prerequisites: Docker ganache container, Node, Java, Maven, jq
echo STARTING DID SERVICE...

REM Compile jar file
set confirmCompile=Y
set /p confirmCompile=Do you need to compile the jar file? (Y/N): (%confirmCompile%)
if /i "%confirmCompile%"=="Y" (
    echo ===========================================================================================
    echo Compiling jar file...
    echo ===========================================================================================
    call mvn clean install -DskipTests
)

REM Start Spring Boot application in a separate console
REM Does not check for updates
@REM mvn install -o 
start "verifier" call java -Dspring.profiles.active=verifier -jar target/did-0.0.1-SNAPSHOT.jar
start "issuer" call java -Dspring.profiles.active=issuer -jar target/did-0.0.1-SNAPSHOT.jar
