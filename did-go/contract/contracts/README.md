# DID contracts

build the go contract file

```sh
# generate the abi
solc --abi contracts/CptContract.sol -o build
solc --abi contracts/DIDContract.sol -o build
# generate evm bytecodes
solc --bin contracts/CptContract.sol -o build
solc --bin contracts/DIDContract.sol -o build
# gen go files
mkdir cpt did
abigen --bin ./build/CptContract.bin --abi ./build/CptContract.abi -pkg=cpt --out=cpt/cpt_contract.go
abigen --bin ./build/DIDContract.bin --abi ./build/DIDContract.abi -pkg=did --out=did/did_contract.go
```

clean

```sh
rm -rf build cpt did
```
