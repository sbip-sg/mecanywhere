from multiprocessing import Process
from multiprocessing.managers import BaseManager
import asyncio
from services.task_consumer import TaskConsumer


class ComputeTask:
    def _run_consumer_in_thread(task_consumer: TaskConsumer) -> None:
        asyncio.run(task_consumer.connect_and_consume())

    def __init__(self) -> None:
        self._process = None
        BaseManager.register("TaskConsumer", TaskConsumer)
        self.task_consumer_manager = BaseManager()
        self.task_consumer_manager.start()
        self.task_consumer = self.task_consumer_manager.TaskConsumer()

    def start(self) -> None:
        self._process = Process(
            target=ComputeTask._run_consumer_in_thread, args=(self.task_consumer,)
        )
        self._process.start()

    def terminate(self) -> None:
        self.task_consumer.close()
        self.task_consumer_manager.shutdown()
        self._process.join()
