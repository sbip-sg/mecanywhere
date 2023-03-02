from multiprocessing import Queue, Process
import base64
import cloudpickle
from message import ComputeRequest
import asyncio
from result import ResultMapping


class ComputeTask:
    async def poll_for_item(queue: Queue, result_mapping: ResultMapping):
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
                result_mapping.set(id, result)

    def _loop(queue: Queue, result_mapping) -> None:
        asyncio.run(ComputeTask.poll_for_item(queue, result_mapping))

    def __init__(self, result_mapping) -> None:
        self._queue = Queue()
        self._process = Process(target=ComputeTask._loop, args=(
            self._queue, result_mapping))

    def start(self) -> None:
        self._process.start()

    def enqueue(self, task: ComputeRequest) -> None:
        self._queue.put(task)
