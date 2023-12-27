# MECAnywhere Services (Development)

Services: 
- Proxy
    - Host URL: http://sbip-g2.d2.comp.nus.edu.sg:11000
- [PO - Authentication service](#po---authentication-service)
    - Hosted by Parent Organisation to issue VC to users of that PO
    - Host URL: 
        - http://localhost:8000
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/po
    - API Documentation: {host}/docs
- [Cloud - DID & VC verification service](#cloud---did--vc-verification-service)
    - verifier port: 8080, issuer port: 9090
    - Hosted by MECA to provide DID and VC verification services
    - Host URL: 
        - http://localhost:8080, http://localhost:9090
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/did-verifier, http://sbip-g2.d2.comp.nus.edu.sg:11000/did-issuer
    - API Documentation: {host}/swagger-ui
- [Full Node - Discovery & Transaction service](#full-node---discovery--transaction-service)
    - discovery port: 7000, transaction port: 7001
    - Hosted on the edge to provide MECA service for end users
    - Host URL: 
        - http://localhost:7000, http://localhost:7001
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/fn-discovery, http://sbip-g2.d2.comp.nus.edu.sg:11000/fn-transaction
    - API Documentation: {host}/docs
- [Cloud - Payment service](#cloud---payment-service)
    - Hosted by MECA to provide payment service for POs
    - Host URL: 
        - http://localhost:7002
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/payment
    - API Documentation: {host}/docs
- Server-host
    - Hosted on the edge to ensure availability of hosts
    - No host URL

Smart contracts:
1. `did/contract/contracts/DIDContract.sol`, `did/contract/contracts/CptContract.sol`: used by verifier and issuer services
2. `full_node/contract/contracts/PaymentContract.sol`: used by payment and transaction services
3. `full_node/contract/contracts/DiscoveryContract.sol`: used by discovery service

Architecture:
https://www.figma.com/file/eBlw4rqX7MT3He8O4t7nxI/MECAnywhere-Architecture-Diagram?type=whiteboard&node-id=0%3A1&t=IANJCjD1wgNtEChu-1

# Configuration

Options: manual, docker local / sbip server (recommended), docker testnet

### Changing environments
See [commit 568f67d](https://github.com/sbip-sg/mec_anywhere/commit/568f67d3cdf600b557f4410c28a29c6b0cfa2f23)
- For manual:
    - `"environment": "development"` in `config.json` for python services.
    - For java services, just use the `verifier` or `issuer` profiles when activating the profile.
- For docker local:
    - `"environment": "docker_local"` in `config.json` for python services. 
    - For java services, include `docker_local` when activating the profile. (default in dockerfile)
- For docker testnet:
    - `"environment": "docker_testnet"` in `config.json` for python services. 
    - For java services, include `docker_testnet` when activating the profile.
    - You may comment out the ganache service in `compose.yaml` since it is not used.

### Secret keys
- For manual:
    - Secret keys can be loaded in `.env` in each service folder. Follow the `.env.example` file for the required variables. 
- For docker local/testnet:
    - Secret keys are loaded by creating a `keys` folder in this base directory where `compose.yaml` is. Each file contains the secret key and the file name is the name of the secret. Required variables are shown in `compose.yaml`. 
        - For python services, you have to add your variables in the settings class in `config.py` too.

### Contracts

> 1. `did/contract/contracts/DIDContract.sol`, `did/contract/contracts/CptContract.sol`: used by verifier and issuer services
> 2. `full_node/contract/contracts/PaymentContract.sol`: used by payment and transaction services
> 3. `full_node/contract/contracts/DiscoveryContract.sol`: used by discovery service

- For all configurations, you still **need to truffle migrate** the contracts to local ganache or sepolia testnet because I'm not able automate it on docker.
- Starting or restarting ganache will reset the blockchain so the smart contracts will need to be redeployed and their addresses should be the same, otherwise update the addresses in each config. 
- For docker local:
    - `truffle migrate --network development`
    - Migrate the DID contracts first, then the full node contracts to correspond to the default config addresses.
- For docker testnet:
    - `truffle migrate --network sepolia`

### Development
In sbip servers, run `docker-compose -f docker-compose-sbip.yaml up -d --no-deps --build {service name}` to rebuild a specific service.
Use `docker-compose-proxy.yaml` to run the nginx set to proxy services in node `worker-111`.

# Quick Start
1. Run docker services
- `docker-compose up` to start all services as containers. Run `docker-compose up --build <service_name>` to rebuild a specific service.
> [!NOTE]  
> Hot reload is enabled for the python services but not the java services. 

2. Migrate the contracts onto your chosen blockchain.
- For development, run `truffle migrate` in the `did/contract` and `full_node/contract` folders to deploy those contracts to ganache that is launched with the docker compose group.
- OR run `load_po.bat` which automates migration of the contracts and loads a standard PO onto the blockchain.

# Manual Start

> [!NOTE]  
> This is no longer recommended as we move towards production.

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
venv/bin/activate
pip install -r requirements.txt
```

### Usage

Run `auth-startup.bat` or run the python service
```
venv/bin/activate
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
venv/bin/activate
pip install -r requirements-local.txt
```

### Usage

Either run the `fullnode-startup.bat` file or follow the instructions below

1. Deploy the smart contracts in the contract folder
2. Run the python service in the discovery folder
```
cd /contract
truffle migrate --network development
cd ../discovery
venv/bin/activate
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
