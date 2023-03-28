from abc import ABC, abstractmethod
from typing import Optional
import multiprocessing


class ResultMapping(ABC):
    @abstractmethod
    def set(self, key, value) -> None:
        pass

    @abstractmethod
    def get(self, key) -> Optional[str]:
        pass


class InMemoryResultMapping(ResultMapping):
    def __init__(self) -> None:
        self._m = multiprocessing.Manager().dict()

    def set(self, key: str, value: str) -> None:
        print("set {} -> {}".format(key, value))
        self._m[key] = value

    def get(self, key: str) -> Optional[str]:
        return self._m.get(key, None)
