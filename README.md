# MECAnywhere Services (Development)

Table of Contents

* [Overview](#overview)
* [Quick Start](#quick-start)
* [Configuration](#configuration)
    * [Changing environments](#changing-environments)
    * [Secret keys](#secret-keys)
    * [Contracts](#contracts)
    * [Serving on SBIP Servers](#serving-on-sbip-servers)


# Overview

### Architecture
<https://www.figma.com/file/eBlw4rqX7MT3He8O4t7nxI/MECAnywhere-Architecture-Diagram?type=whiteboard&node-id=0%3A1&t=IANJCjD1wgNtEChu-1>
<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="750" height="450" src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FeBlw4rqX7MT3He8O4t7nxI%2FMECAnywhere-Architecture-Diagram%3Ftype%3Dwhiteboard%26node-id%3D0%253A1%26t%3DKMSVEWp4c3UO9Rgy-1" allowfullscreen></iframe>

### Services

> Open `docs/build/index.html` to view the offline API documentation.

- Proxy
    - Host URL: http://sbip-g2.d2.comp.nus.edu.sg:11000
- PO - Authentication service
    - Hosted by Parent Organisation to issue VC to users of that PO
    - Host URL: 
        - http://localhost:8000
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/po
    - API Documentation: {host}/docs
- Cloud - DID & VC verification service
    - verifier port: 8080, issuer port: 9090
    - Hosted by MECA to provide DID and VC verification services
    - Host URL: 
        - http://localhost:8080, http://localhost:9090
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/did-verifier, http://sbip-g2.d2.comp.nus.edu.sg:11000/did-issuer
    - API Documentation: {host}/swagger-ui
- Full Node - Discovery & Transaction service
    - discovery port: 7000, transaction port: 7001
    - Hosted on the edge to provide MECA service for end users
    - Host URL: 
        - http://localhost:7000, http://localhost:7001
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/fn-discovery, http://sbip-g2.d2.comp.nus.edu.sg:11000/fn-transaction
    - API Documentation: {host}/docs
- Cloud - Payment service
    - Hosted by MECA to provide payment service for POs
    - Host URL: 
        - http://localhost:7002
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/payment
    - API Documentation: {host}/docs
- Server-host
    - Hosted on the edge to ensure availability of hosts
    - No host URL
- Ganache
    - Blockchain for development
    - Host URL: 
        - http://localhost:8545
        - http://sbip-g2.d2.comp.nus.edu.sg:11011

### Smart contracts
1. `did/contract/contracts/DIDContract.sol`, `did/contract/contracts/CptContract.sol`: used by verifier and issuer services
2. `full_node/contract/contracts/PaymentContract.sol`: used by payment and transaction services
3. `full_node/contract/contracts/DiscoveryContract.sol`: used by discovery service

# Quick Start (local)
> If starting fresh on SBIP servers, see [serving on SBIP servers](#serving-on-sbip-servers).

1. Configure keys/env variables (see [Configuration -> Secret keys](#secret-keys))

2. Run docker services
- `docker-compose up` to start all services as containers. Run `docker-compose up --build <service_name>` to rebuild a specific service.
> [!NOTE]  
> Hot reload is enabled for the python services but not the java services. 

3. Migrate the contracts onto your chosen blockchain.
- For development, run the commands in [Contracts](#contracts) in the `did/contract` and `full_node/contract` folders to deploy those contracts to ganache that is launched with the docker compose group.
> Requirements: truffle
- OR run `load_po.bat` which automates migration of the contracts and loads a standard PO onto the blockchain.
> Requirements: truffle, python


# Configuration

Options: manual, docker local / sbip server (recommended), docker testnet

### Changing environments
> See [commit 568f67d](https://github.com/sbip-sg/mec_anywhere/commit/568f67d3cdf600b557f4410c28a29c6b0cfa2f23)
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
    - Secret keys are loaded by creating a `keys` folder in this base directory where `compose.yaml` is. Each file contains the secret key and the file name is the name of the secret. Required variables are shown in [`compose.yaml`](compose.yaml). 
        - For python services, you have to add your variables in the settings class in `config.py` too.

#### List of keys
> Format: _key: value_
> See compose files for the dependent services of each key.
- `0x52c...`(DID of issuer for did-issuer service): private key
- `access_token_key.txt`: secret key for encoding the jwt access token
- `refresh_token_key.txt`: secret key for encoding the jwt refresh token
- `server_host_did.txt`: arbitrary string used as DID of the server host
- `server_host_name.txt`: arbitrary string used as name of the server host
- `server_host_po_did.txt`: arbitrary string used as DID of the server host's PO
- `wallet_address.txt`: address of the wallet/account for services that calls the smart contracts
- `wallet_private_key.txt`: private key of the wallet/account for services that calls the smart contracts

### Contracts

[List of contracts](#smart-contracts)

- For all configurations, you still **need to truffle migrate** the contracts to local ganache or sepolia testnet because I'm not able automate it on docker.
- Starting or restarting ganache will reset the blockchain so the smart contracts will need to be redeployed and their addresses should be the same, otherwise update the addresses in each config. 
- For docker local:
    ```
    truffle migrate --network development
    ```
    - Migrate the DID contracts first, then the full node contracts to correspond to the default config addresses.
- For docker testnet:
    ```
    truffle migrate --network sepolia
    ```

### Serving on SBIP Servers
We use `docker-compose-sbip.yaml` for production configuration instead of `compose.yaml`.

On sbip servers, run 
```
docker compose -f docker-compose-sbip.yaml up -d --no-deps --build {service name}
``` 
to rebuild a specific service.

Use `docker-compose-proxy.yaml` to run the nginx on the main node by running 
```
docker compose -f docker-compose-proxy.yaml up -d
```
and it is set to proxy services in node `worker-111`.

Migrate the contracts to this ganache by running
```
truffle migrate --network docker_sbip
```
in each contract folder. Basically do `load_po.bat` but with `docker_sbip` network configured in `truffle-config.js`.
