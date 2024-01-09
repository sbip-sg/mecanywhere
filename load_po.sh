#!/bin/bash

cd did/contract
truffle migrate --network development
cd ../..

cd full_node/contract
truffle migrate --network development
cd ../..

python load_po.py
