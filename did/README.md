# DID Service

## Description

## Table of Contents

- [DID Service](#did-service)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Getting started](#getting-started)
  - [Usage](#usage)
  - [Important files and folders](#important-files-and-folders)
  - [Future improvements](#future-improvements)

## Requirements

1. Java

```
sudo apt install openjdk-11-jdk maven
```

2. Node and npm

Refer to the official website for intallation instructions https://nodejs.org/en/download/

3. Docker

Refer to the official website for intallation instructions https://docs.docker.com/get-docker/

4. Ganache

There are multiple ways to install ganache, but I personally prefer using docker.

`docker pull trufflesuite/ganache-cli`

Refer to the official website for alternative options https://github.com/trufflesuite/ganache

5. truffle

`npm install -g truffle`

Refer to the official website for more information https://github.com/trufflesuite/truffle

## Getting started

1. Start a local ethereum network by running the following command.

```
sudo docker run -p 8545:8545 --name ganache -d trufflesuite/ganache-cli:latest --mnemonic "baby blame blast picnic asthma topic guilt lock shoulder humble fortune control" --gasLimit=9000000
```

2. Create an environment file `.env` in `resources` folder with the first private key from the pre-generated list of accounts from the previous step (remoe `-d` option in the first step to see the results). This private key will be used to execute and sign transactions on the blockchain.

```
echo "WALLET_PRIVATE_KEY=0x0d8c2fee2d85f6f8dc47f36da23ea1fd29b1126c48bac505d159bbf3f3c8e0bf" > src/main/resources/.env
```

3. Also create another `.env` file con `contract` folder. This will be used in the smart contract deployment step.

```
echo "IS_DEVELOPMENT=true" > contract/.env
echo 'MNEMONIC="baby blame blast picnic asthma topic guilt lock shoulder humble fortune control"' >> contract/.env
echo "WALLET_PRIVATE_KEY=0x0d8c2fee2d85f6f8dc47f36da23ea1fd29b1126c48bac505d159bbf3f3c8e0bf" >> contract/.env
```

4. Deploy the smart contract on the blockchain.

```
cd contract
npm install
truffle migrate --network development
```

5. Build and run the java source code

```
# Build the source code
mvn clean install

# Start a process that runs the DID service on port 80
sudo java -Dspring.profiles.active=didservice -jar target/did-0.0.1-SNAPSHOT.jar &

# Start a process that runs the issuer on port 8080
sudo java -Dspring.profiles.active=issuer -jar target/did-0.0.1-SNAPSHOT.jar &

# Alternatively, simnply run both the DID service and the issuer on port 8080
sudo java -jar target/did-0.0.1-SNAPSHOT.jar &
```

6. Register the issuer

```
# We started a fresh local blockchain network, so we need to register an issuer. This will register a DID did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8 that we will use as the issuer.

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{ "publicKey": 4261665221056439992349256207169667065315027578390647705456165282391832261498313490844998910722927847484140730450920258944230161311480552650871661291293643}' \
  http://<did-service-ip:port>/api/v1/did/create
```

7. Create 'keys' directory in the did folder. Make sure to copy the issuer's example private key in the `keys` directory, otherwise you will not be able to issue credentials.

```
 cp 0xfd340b5a30de452ae4a14dd1b92a7006868a29c8.example keys/0xfd340b5a30de452ae4a14dd1b92a7006868a29c8
```

8. (Optional) You can view Swagger API specification by go to the following URL(s)

```
# You can view the Swagger API specification at <ip:port>/swagger-ui

# For example, to view the Swagger API specification for the DID service running on localhost on port 80

http://localhost:80/swagger-ui

# To view the Swagger API specification for the issuer service running on localhost on port 8080

http://localhost:8080/swagger-ui
```

8. (Optional) Build Docker container for deployment (SBIP Server)

```
# Under the current settings, port 9006 is reserved for the did service and 9007 for the issuer service. 

# Make sure did-0.0.1-SNAPSHOT.jar is build and in the target folder

# Run docker build commands in the did directory. Build 2 docker files, DockerFile2 for did service and DockerFile3 for issuer

cd did
docker build -f DockerFile2 -t verifier .
docker build -f DockerFile3 -t issuer .

docker run -d -p 8080:8080 verifier
docker run -d -p 9090:9090 issuer

```

## Usage

1. To create and register a DID, you can invoke `POST /api/v1/did/create` endpoint and supply `publicKey` in Big Integer format in the request body. If you do not have a public key to use, to can invoke `GET /api/v1/did/genkey` to generate a new keypair that you can use. Note that `GET /api/v1/did/genkey` is meant to be used for testing purposes only.

2. To read a DID Document, you can invoke `GET /api/v1/did/document/{DID}` to read the entire DID Document associated with a DID.

3. There are multiple opeartions that we can do with a DID. For example, you can invoke `POST /api/v1/did/addPublicKey` to add a new public key to the DID and invoke `POST /api/v1/did/addAuthentication` to add a new authentication. However, we do not often use them in the project. If you find a need to use these operations in the future, most of the operations should be somewhat ready to use already.

4. Before issuing any credentials, you must register a CPT. To register a CPT, you can invoke `/api/v1/cpt/register`, specify the schema of the CPT in the request body, and specify the `publisher` DID which should be `did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8` if you followed the steps in [Getting Started](#getting-started).

5. To issue a credential, you can invoke `/api/v1/credential/create` with the credential you want to issue in the request body under `claimData` filed, the `cptId` you obtained from the previous step, and the `issuer` DID. The entire object under `result` field in the actual credential that you can use.

6. To verify a credential, invoke `/api/v1/credential/verify` with the entire credential you want to verify under `credential` field in the request body. The returned response will be `true` if the credential is valid or `false` if it is invalid.

7. A verifiable presentation is signed by the holder of the credential, thus it should be created and signed on the client side, typically in Javascript. Sign the json body of the presentation without the proof section. You may use the `crypto-js` and `secp256k1` libraries in Javascript to sign it like so:

```
const hash = Buffer.from(CryptoJS.SHA3(message, { outputLength: 256 }).toString(CryptoJS.enc.Hex), 'hex');
const signature = secp256k1.ecdsaSign(hash, hexToUtf8(privateKey));
```

## Important files and folders

- The components in `src/main/java/meca/did/controller` serve mainly as a mediator between users (requests) and applications. They perform minimal business logic before forwarding the requests to the service layer.

- The components (except Engines) in `src/main/java/meca/did/service` serve as the service layer that perform the main logic such as generate a DID and compute a hash. After that the requests will be forwarded to the data access layer, engines in this case.

- The engines are the components that interact with the blockchain through smart contracts. The configurations such as smart contract addresses and binaries are defined in `src/main/java/meca/did/contract`

- The classes in `src/main/java/meca/did/protocol` mainly define the models that we use throughout the program lifecycle.

- The general configurations such as port number are located `src/main/resources/` folder.

- The ethreum smart contracts are located in `contract` folder.

- The error codes and thier description returned in the responses are defined in `src/main/java/meca/did/constant/ErrorCode.java`

## Future improvements

1. The security has not been considered and addressed in the current implementation. You can use popular frameworks such as Spring Security to enhance the security and limit users who can invoke the APIs.

2. Microservice architecture can be considered if there is a need to scale up efficiently in the future.

3. The current implementation only uses local blockchain. If we want to roll out this DID framework, we might need to consider using global blockchain networks or possibly other blockchain platforms such as solana to save costs.

4. The codebase is in the same repo with the backend. You might also consider to seperate the code to another standalone repo.

5. If you update or modify the smart contracts, the smart contract addresses and bytecodes will change. So, you need to update them accordingly.

```
# To get the smart contract detail, navigate to the contract directory

cd contract

truffle console

let x = await <Name-of-smart-contract>.deployed()

# For example

let x = await DIDContract.deployed()

x

# You should see the smart contract address in `address` field and bytecode `bytecode` field.

# Then you should update the properties defined in src/main/resources/application.properties, src/main/resources/application-didservice.properties, and src/main/resources/application-issuer.properties accordingly.
```

6. I developed the code based on [WeIdentity Sample](https://github.com/WeBankBlockchain/WeIdentity-Sample) and [WeIdentity Contract](https://github.com/WeBankBlockchain/WeIdentity-Contract). Refer to the original source code for your reference if needed.
