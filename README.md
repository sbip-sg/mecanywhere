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
- [Full Node - Discovery & Transaction service](#full-node---discovery--transaction-service)
    - discovery port: 7000, transaction port: 7001
    - Hosted on the edge to provide MECA service for end users
    - API Documentation: http://localhost:7000/docs and http://localhost:7001/docs
- [Cloud - Payment service](#cloud---payment-service)
    - port: 7002
    - Hosted by MECA to provide payment service for POs
    - API Documentation: http://localhost:7002/docs

Architecture:
https://www.figma.com/file/eBlw4rqX7MT3He8O4t7nxI/MECAnywhere-Architecture-Diagram?type=whiteboard&node-id=0%3A1&t=IANJCjD1wgNtEChu-1

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

Run `auth-startup.bat` or run the python service
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


## Full Node - Discovery & Transaction service

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
3. Do the same in the transaction folder


## Cloud - Payment service

### Requirements
- python3
- node
- docker ganache container

### Installation

1. Install python and copy the payment contract build file from full_node/contract after compiling it
```
cd payment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../full_node/contract
truffle migrate --network development
```

### Usage

Run `payment-startup.bat` or follow the instructions below
```
source venv/bin/activate
cd src
uvicorn main:app --port 7002 --reload
```
