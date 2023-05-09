# Full Node (development)

## Requirements
- python3
- node
- docker ganache container

## Installation

1. Compile the smart contracts in the contract folder
2. Install python and its relevant packages
```
cd full_node/contract
npm install
cd ../discovery
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Either run the `windows-startup.bat` file or follow the instructions below

1. Deploy the smart contracts in the contract folder
2. Run the python service in the discovery folder
```
docker start ganache
cd full_node/contract
truffle migrate --network development
cd ../discovery
source venv/bin/activate
cd src
uvicorn main:app --port 7000 --workers 1 --reload
```
