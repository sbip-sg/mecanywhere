# MECAnywhere Services (Development)

Services: 
- [PO - Authentication service](#po---authentication-service)
    - port 8000
    - Hosted by Parent Organisation to issue VC to users of that PO
    - API Documentation: http://localhost:8000/docs
- [Cloud - DID & VC verification service](#cloud---did--vc-verification-service)
    - verifier port: 8080, issuer port: 9090
    - Hosted by MECA to provide DID and VC verification services
    - API Documentation: http://localhost:8080/swagger-ui and http://localhost:9090/swagger-ui
- [Full Node - Discovery service](#full-node---discovery-service)
    - port: 7000
    - Hosted by MECA to provide discovery service for end users
    - API Documentation: http://localhost:7000/docs

## Quick Start
Run `startup.bat` to start all the services. Sorray theres no docker version yet.

# Manual Start

## Pre-requisites
- running ganache container
- running local rabbitmq service

## PO - Authentication service

### Requirements
- python3

### Installation

Install python and its relevant packages
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage

Run the python service
```
source venv/bin/activate
uvicorn main:app --port 8000 --reload
```


## Cloud - DID & VC verification service

### Requirements
- java
- maven
- node
- docker ganache container

### Installation

1. Install the necessary node packages for compiling the smart contracts in the contract folder
```
cd contract
npm install
```
2. Build jar file: `mvn clean install`

### Usage
Run `did-local-startup.bat` or follow the instructions below
```
cd /contract
truffle migrate --network development
cd ..
java -Dspring.profiles.active=verifier -jar target/did-0.0.1-SNAPSHOT.jar
java -Dspring.profiles.active=issuer -jar target/did-0.0.1-SNAPSHOT.jar
```


## Full Node - Discovery service

### Requirements
- python3
- node
- docker ganache container
- rabbitmq

### Installation

1. Install the necessary node packages for compiling the smart contracts in the contract folder
2. Install python and its relevant packages
```
cd full_node/contract
npm install
cd ../discovery
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage

Either run the `fullnode-startup.bat` file or follow the instructions below

1. Deploy the smart contracts in the contract folder
2. Run the python service in the discovery folder
```
cd /contract
truffle migrate --network development
cd ../discovery
source venv/bin/activate
cd src
uvicorn main:app --port 7000 --reload
```
