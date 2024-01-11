#!/bin/bash

cd did/contract
truffle migrate --network development
# truffle migrate --network docker_sbip
cd ../..

cd full_node/contract
truffle migrate --network development
# truffle migrate --network docker_sbip
cd ../..

python load_po.py localhost:8080 localhost:9090
# python load_po.py sbip-g2.d2.comp.nus.edu.sg:11000/did-verifier sbip-g2.d2.comp.nus.edu.sg:11000/did-issuer
