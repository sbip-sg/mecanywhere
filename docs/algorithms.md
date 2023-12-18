# Algorithms

## Offloading

Offloading occurs asynchronously and results are received in a separate process saved to cache. The SDK allows synchronous offloading by calling the `join` function immediately after an offload (see sdk documentation in desktop repo).

The flow of offloading a task looks like this:

1. Client calls `offload` and the first available host (has free resources and not timed out) is selected. At the same time, its record of available resources will be subtracted according to the task resource limits. The task is published to the host's queue via the publishing queue in the main process. Cache records the published host.
2. Host retrieves task from its queue and starts executing it.
3. Host finishes executing the task and publishes the result to the result queue residing in a separate backend process, which achieves asynchronous rpc. The record of available resources is added back to the published host recorded in the cache.
4. If offload fails, record of available resources are restored.
5. If cache record fails, restoration of available resources will fail. In this case, a host might not be fully utilized since its record will be lower than the actual. As a fallback, the heartbeat of the host will reset the resource limits when the host is fully idle.
6. If server-host is used as the host, available resources will not be tracked.