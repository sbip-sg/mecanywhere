from abc import ABC, abstractmethod
from typing import Optional


class ResultMapping(ABC):
    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass


class InMemoryResultMapping(ResultMapping):
    def __init__(self) -> None:
        self._m = {}

    def set(self, key: str, value: str) -> None:
        self._m[key] = value

    def get(self, key: str) -> Optional[str]:
        return self._m.get(key, None)
