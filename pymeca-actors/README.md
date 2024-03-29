# Setup

## Template actors
```
docker build -t mock_actor -f Dockerfile .

For user and tower:
docker run -it --rm mock_actor mock_user.py
docker run -it --rm mock_actor mock_tower.py

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
