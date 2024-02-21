# MECAnywhere Services (Development)

Table of Contents

* [Overview](#overview)
* [Quick Start](#quick-start)
* [Configuration](#configuration)
    * [Changing environments](#changing-environments)
    * [Secret keys](#secret-keys)
    * [Serving on SBIP Servers](#serving-on-sbip-servers)


# Overview

### Services

> Open `docs/build/index.html` to view the offline API documentation.

- Proxy
    - Host URL: http://sbip-g2.d2.comp.nus.edu.sg:11000
- Full Node (tower) - Discovery service
    - discovery port: 7000
    - Hosted on the edge to provide MECA service for end users
    - Host URL: 
        - http://localhost:7000
        - http://sbip-g2.d2.comp.nus.edu.sg:11000/fn-discovery
    - API Documentation: {host}/docs
- Blockchain
    - Blockchain for development
    - Host URL: 
        - http://localhost:8545
        - http://sbip-g2.d2.comp.nus.edu.sg:11011


# Quick Start (local)
> If starting fresh on SBIP servers, see [serving on SBIP servers](#serving-on-sbip-servers).

1. Configure keys/env variables (see [Configuration -> Secret keys](#secret-keys))

2. Run docker services
- `docker-compose up` to start all services as containers. Run `docker-compose up --build <service_name>` to rebuild a specific service.
> [!NOTE]  
> Hot reload is enabled for the python services.


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
    - You may comment out the blockchain service in `compose.yaml` since it is not used.

### Secret keys
- For manual:
    - Secret keys can be loaded in `.env` in each service folder. Follow the `.env.example` file for the required variables. 
- For docker local/testnet:
    - Secret keys are loaded by creating a `keys` folder in this base directory where `compose.yaml` is. Each file contains the secret key and the file name is the name of the secret. Required variables are shown in [`compose.yaml`](compose.yaml). 
        - For python services, you have to add your variables in the settings class in `config.py` too.

#### List of keys
> Format: _key: value_
>
> See compose files for the dependent services of each key.
- `wallet_address.txt`: address of the wallet/account for services that calls the smart contracts
- `wallet_private_key.txt`: private key of the wallet/account for services that calls the smart contracts


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
