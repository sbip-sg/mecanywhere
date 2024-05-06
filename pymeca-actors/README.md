# Setup

## Containers
- [Template actors - CLI](#template-actors-cli)
- [Template actors - Server](#template-actors-server)
- [IPFS (local isolation)](#ipfs-local-isolation)
- [Task Executor](#task-executor)
- [Tower Server](#tower-server)

## Template actors CLI
First, load `.env`
For running within the same network and with pymeca changes, 
```
docker network create --subnet=172.18.0.0/16 intern_network
docker build -t mock_actor_intern -f DockerfileInternal ..

docker run -it --rm --net intern_network --ip 172.18.0.2 -w /tmp/pymeca/src/pymeca/scripts  mock_actor_intern ganache.py --port 9000 --ganache-server-script-path ../../../meca-contracts/src/ganache/index.js --generate-accounts --accounts_file_path ../../config/accounts.json --dao-address-file-path ../dao_contract_address.txt --dao-file-path ../../../meca-contracts/src/contracts/MecaContract.sol --scheduler-file-path ../../../meca-contracts/src/contracts/SchedulerContract.sol --host-file-path ../../../meca-contracts/src/contracts/HostContract.sol --tower-file-path ../../../meca-contracts/src/contracts/TowerContract.sol --task-file-path ../../../meca-contracts/src/contracts/TaskContract.sol --scheduler-fee 100 --host-register-fee 100 --host-initial-stake 100 --host-task-register-fee 100 --host-failed-task-penalty 100 --tower-initial-stake 100 --tower-host-request-fee 100 --tower-failed-task-penalty 100 --task-addition-fee 100
docker run -it --rm --net intern_network --ip 172.18.0.3 mock_actor_intern tower/src/main.py 7777
docker run -it --rm --net intern_network --ip 172.18.0.4  mock_actor_intern mock_tower.py
docker run -it --rm --net intern_network --ip 172.18.0.5 -v /var/run/docker.sock:/var/run/docker.sock mock_actor_intern mock_host.py
docker run -it --rm --net intern_network --ip 172.18.0.6 -v $PWD/build:/scripts/src/build  mock_actor_intern mock_user.py
docker run -it --rm --net intern_network --ip 172.18.0.7 -v <ABSOLUTE_PATH_TO_FOLDER>:/build mock_actor_intern mock_task_dev.py
```
For general use,
```
docker build -t mock_actor -f Dockerfile .

docker run -it --rm mock_actor mock_tower.py

For user, mount a folder to retrieve task output:
docker run -it --rm -v $PWD/build:/scripts/src/build mock_actor mock_user.py

For task developer, mount a folder for IPFS staging:
docker run -it --rm -v <ABSOLUTE_PATH_TO_FOLDER>:/build mock_actor mock_task_dev.py

For host, mount the docker socket for docker in docker:
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock mock_actor mock_host.py
```

## Template actors Server
First, load `.env`
```
uvicorn server:app
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
If mock_actor_intern image was built, the tower server can be started with that image:
```
docker run -it --rm mock_actor_intern tower/src/main.py 7777
```
Else:

In `../tower`
```
docker build -t tower_server .
docker run -p 7777:7777 tower_server 7777
```
Change `--net`/`--ip`/exposed port if you want.

# Usage

## CLI
Follow prompts

## Server

- `/init_actor/{actor_type}` : Initialize actor of type `actor_type`
    - params:
        - `actor_type`: host / tower / task_dev / user
    - returns:
        - list of methods available to the actor
- `/{function_name}` : Call function `function_name`
    - params:
        - `function_name`: name of the function to call
    - returns:
        - result of the function call

For example:
```
curl -L 'http://localhost:8000/init_actor/host' -X POST -H 'Content-Type: application/json'
curl -L 'http://localhost:8000/register' -X POST -H 'Content-
Type: applcation/json' -d '{"block_timeout_limit": 10, "public_key":"","initial_deposit":100}'
curl -L 'http://localhost:8000/get_my_tasks' -X POST -H 'Content-Type: applcation/json'
```

## Workflow

1. **Tower**: register_as_tower
2. **Task Dev**: add_task
    
    IPFS node should be running

3. **Host**: register_as_host
4. **Host**: get_tasks, add_task
5. **Host**: get_towers, register_for_tower

    Tower Server should be running

6. **Tower**: get_pending_hosts, accept_host
7. **Host**: wait_for_my_task
8. **User**: get_tasks, get_towers_hosts_for_task, send_task
    
    Task Executor should be running

9. **User**: finish_task
