# Tower server

Tower server establishes communication between clients and hosts.

* A client sends to tower the task input and wait for response.
* tower forward the input to the target host and wait for response.
* tower send an acknowledgement to the host.
* response from host is sent back to the client.

## Handling crash failure

When tower server crashes, its connection with client and tower is reset. Client retries sending message to the tower and host retries sending response. Before sending acknowlegement to host for a task output, the tower server persist it. When client retries with its task, tower reply with the persisted result.
