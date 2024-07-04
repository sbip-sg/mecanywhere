# MECAnywhere Services

Table of Contents

* [Overview](#overview)
* [Quick Start](#quick-start)
* [Configuration](#configuration)
    * [Changing environments](#changing-environments)
    * [Secret keys](#secret-keys)


# Overview

This repository contains the services for the MECAnywhere project that are used to interact with pymeca and the smart contracts. Use the pymeca-actors to join the MECAnywhere ecosystem now! 

### Architecture

https://www.figma.com/file/JkjN5hBQYfCFEMpc2QS4eH/MECAnywhere-Architecture-Diagram-(V2)?type=whiteboard&node-id=0%3A1&t=VgoZo4ZXrVZtnZ9s-1

### Services

> Open https://sbip-sg.github.io/mec_anywhere/ for online documentation + user guides.

- did-go
    - Decentalized Identity (DID) service written in Golang
- Tower
    - Hosted on the edge to provide task forwarding for end users
    - [README](tower/README.md)
- Pymeca actors
    - Template actors that use pymeca library to interact with the smart contracts. These come in the form of CLI.
    - [README to setup](pymeca-actors/README.md)
    - User guides in docs

# Quick Start (local)
1. Configure keys/env variables (see [Configuration -> Secret keys](#secret-keys))

2. Pull submodules with `git submodule update --init --recursive` in `pymeca` folder.

3. Run docker services
- `docker-compose up` to start all services as containers. 
- `docker-compose up --build <service_name>` to rebuild a specific service.
- \+ `-f docker-compose-internal.yaml` is for working with pymeca library changes.
- \+ `-f docker-compose.yaml` is for working with pymeca version from pypi.

# Configuration

Options: manual, docker local (recommended), docker testnet

### Secret keys
- For manual:
    - Secret keys can be loaded in `.env` in each service folder. Follow the `.env.example` file for the required variables. 
- For docker local/testnet:
    - Secret keys are loaded by creating a `keys` folder in this base directory where `compose.yaml` is. Each file contains the secret key and the file name is the name of the secret. Required variables are shown in [`compose.yaml`](compose.yaml). 
        - For python services, you have to add your variables in the settings class in `config.py` too.

#### List of keys
> Format: _key: value_

> See compose files for the dependent services of each key.
- `tower_private_key.txt`: private key of the wallet/account for tower actor that calls the smart contracts
