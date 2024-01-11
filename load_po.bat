@echo off

cd did\contract
call truffle migrate --network development
@REM call truffle migrate --network docker_sbip
cd ..\..

cd full_node\contract
call truffle migrate --network development
@REM call truffle migrate --network docker_sbip
cd ..\..

python util/load_po.py localhost:8080 localhost:9090
@REM python util/load_po.py sbip-g2.d2.comp.nus.edu.sg:11000/did-verifier sbip-g2.d2.comp.nus.edu.sg:11000/did-issuer
