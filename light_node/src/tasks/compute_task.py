from multiprocessing import Queue, Process
import queue as python_queue
import base64
import cloudpickle
import asyncio
from models.message import ComputeRequest
from models.result import ResultMapping


class ComputeTask:
    async def poll_for_item(self, queue: Queue, result_mapping: ResultMapping):
        while self._loop_running.is_set():
            await asyncio.sleep(0.05)
            try:
                item = queue.get_nowait()
            except python_queue.Empty:
                continue
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

    def _loop(self, queue: Queue, result_mapping) -> None:
        asyncio.ensure_future(self.poll_for_item(queue, result_mapping))

    def __init__(self, result_mapping) -> None:
        self._queue = Queue()
        self._loop_running = asyncio.Event()
        self._loop_running.set()
        self._process = Process(target=self._loop, args=(self._queue, result_mapping))

    def start(self) -> None:
        self._process.start()

    def enqueue(self, task: ComputeRequest) -> None:
        self._queue.put(task)

    async def terminate(self) -> None:
        self._queue.close()
        self._loop_running.clear()
        self._queue.join_thread()
        self._process.join()
