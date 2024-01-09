Algorithms
==========

Offloading
----------

Offloading occurs asynchronously and results are received in a separate process saved to cache. The SDK allows synchronous offloading by calling the ``join`` function immediately after an offload (see sdk documentation in desktop repo).

The flow of offloading a task looks like this:

1. Client calls offload and the first available host (has free resources and not timed out) is selected. At the same time, its record of available resources will be subtracted according to the task resource limits. The task is published to the host's queue via the publishing queue in the main process. Cache records the published host.
2. Host retrieves task from its queue and starts executing it.
3. Host finishes executing the task and publishes the result to the result queue residing in a separate backend process, which achieves asynchronous rpc. The record of available resources is added back to the published host recorded in the cache.

   - If offload fails, record of available resources are restored (added back).
   - If cache record fails, restoration of available resources will fail. In this case, a host might not be fully utilized since its record will be lower than the actual. No fallback is implemented for this case (yet).

     - Heartbeat is not used to track available resources because task executor might not be executing but resources are used in maintaining container for some idle time - should still post tasks to this host.

   - If server-host is used as the host, available resources will not be tracked.

4. Result queue consumes the result and saves it to cache.
5. Server polls the cache and retrieves the result. The result is then sent to the client.
