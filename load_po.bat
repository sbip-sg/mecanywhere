@echo off

cd did\contract
call truffle migrate --network development
cd ..\..

cd full_node\contract
call truffle migrate --network development
cd ..\..

python load_po.py
