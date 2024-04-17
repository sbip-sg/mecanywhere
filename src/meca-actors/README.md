# Setup

## Template actors
```
docker network create --subnet=172.18.0.0/16 intern_network

ganache.py --port 9000 --ganache-server-script-path ../../../meca-contracts/src/ganache/index.js --accounts_file_path ../../config/accounts.json --dao-address-file-path ../dao_contract_address.txt --dao-file-path ../../../meca-contracts/src/contracts/MecaContract.sol --scheduler-file-path ../../../meca-contracts/src/contracts/SchedulerContract.sol --host-file-path ../../../meca-contracts/src/contracts/HostContract.sol --tower-file-path ../../../meca-contracts/src/contracts/TowerContract.sol --task-file-path ../../../meca-contracts/src/contracts/TaskContract.sol --scheduler-fee 100 --host-register-fee 100 --host-initial-stake 100 --host-task-register-fee 100 --host-failed-task-penalty 100 --tower-initial-stake 100 --tower-host-request-fee 100 --tower-failed-task-penalty 100 --task-addition-fee 100

docker build -t mock_actor -f Dockerfile .
docker build -t mock_actor_intern -f DockerfileInternal ../..
docker run -it --rm --net intern_network --ip 172.18.0.2 -w /tmp/pymeca/src/pymeca/scripts  mock_actor_intern ganache.py --port 9000 --ganache-server-script-path ../../../meca-contracts/src/ganache/index.js --accounts_file_path ../../config/accounts.json --dao-address-file-path ../dao_contract_address.txt --dao-file-path ../../../meca-contracts/src/contracts/MecaContract.sol --scheduler-file-path ../../../meca-contracts/src/contracts/SchedulerContract.sol --host-file-path ../../../meca-contracts/src/contracts/HostContract.sol --tower-file-path ../../../meca-contracts/src/contracts/TowerContract.sol --task-file-path ../../../meca-contracts/src/contracts/TaskContract.sol --scheduler-fee 100 --host-register-fee 100 --host-initial-stake 100 --host-task-register-fee 100 --host-failed-task-penalty 100 --tower-initial-stake 100 --tower-host-request-fee 100 --tower-failed-task-penalty 100 --task-addition-fee 100
docker run -it --rm --net intern_network --ip 172.18.0.3  mock_actor_intern tower_websocket.py 7777
docker run -it --rm --net intern_network --ip 172.18.0.4  mock_actor_intern mock_tower.py
docker run -it --rm --net intern_network --ip 172.18.0.5  mock_actor_intern mock_host.p
docker run -it --rm --net intern_network --ip 172.18.0.6  mock_actor_intern mock_user.py
docker run -it --rm --net intern_network --ip 172.18.0.7  mock_actor_intern mock_task_dev.py
For user and tower:
docker run -it --rm mock_actor mock_user.py
docker run -it --rm mock_actor mock_tower.py
docker run -it --rm -p 7777:7777 mock_actor tower_websocket.py

For task developer, mount a folder for IPFS staging:
docker run -it --rm -v <ABSOLUTE_PATH_TO_FOLDER>:/build mock_actor mock_task_dev.py

For host, mount the docker socket for docker in docker:
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock mock_actor mock_host.py
```

## IPFS (local isolation)
Start IPFS node if you want to upload (task developer) folders. The node where the host downloads from should be accessible from the node the task developer uploads to. i.e. They could be the same node or accessed from a public gateway.

The IPFS node can be started with docker with the following commands:
```
export ipfs_staging=</ABSOLUTE/PATH/TO/SOMEWHERE/>
docker run -d --name ipfs_host -v $ipfs_staging:/export -p 4001:4001 -p 4001:4001/udp -p 127.0.0.1:8080:8080 -p 127.0.0.1:5001:5001 ipfs/kubo:latest
```
Staging path refers to directory with the files to be uploaded.

## Task Executor
Start task executor for the host to execute tasks.

## Tower Server
Start tower server to relay tasks from client to host.
