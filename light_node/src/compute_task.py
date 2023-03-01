from multiprocessing import Queue, Process
import base64
import cloudpickle
from message import ComputeRequest
import asyncio
from update_strategy import UpdateStrategy


class ComputeTask:
    async def poll_for_item(queue: Queue, update_strategy: UpdateStrategy):
        while True:
            await asyncio.sleep(0.05)
            item = queue.get()
            id = item.id
            func_binary = item.binary
            result = None
            try:
                func = base64.b64decode(func_binary)
                result = cloudpickle.loads(func)()
            except:
                result = ""
            finally:
                data = {'id': id, 'result': result}
                asyncio.create_task(update_strategy.update(data))

    def _loop(queue: Queue, update_strategy) -> None:
        asyncio.run(ComputeTask.poll_for_item(queue, update_strategy))

    def __init__(self, update_strategy) -> None:
        self._queue = Queue()
        self._update_strategy = update_strategy
        self._process = Process(target=ComputeTask._loop, args=(
            self._queue, self._update_strategy))

    def start(self) -> None:
        self._process.start()

    def enqueue(self, task: ComputeRequest) -> None:
        self._queue.put(task)
