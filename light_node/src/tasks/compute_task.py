from multiprocessing import Queue, Process, Value
import queue as python_queue
import base64
import cloudpickle
import asyncio
from models.message import ComputeRequest
from models.result import ResultMapping


class ComputeTask:
    async def poll_for_item(
        self, loop_running: bool, queue: Queue, result_mapping: ResultMapping
    ):
        while loop_running.value:
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

    def _loop(self, loop_running: bool, queue: Queue, result_mapping) -> None:
        asyncio.run(self.poll_for_item(loop_running, queue, result_mapping))

    def __init__(self, result_mapping) -> None:
        self._queue = Queue()
        self._loop_running = Value("b", True)
        self.result_mapping = result_mapping
        self._process = None

    def start(self) -> None:
        self._process = Process(
            target=self._loop,
            args=(self._loop_running, self._queue, self.result_mapping),
        )
        self._process.start()

    def enqueue(self, task: ComputeRequest) -> None:
        self._queue.put(task)

    def terminate(self) -> None:
        self._queue.close()
        self._loop_running.value = False
        self._queue.join_thread()
        self._process.join()
