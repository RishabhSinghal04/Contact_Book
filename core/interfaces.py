from abc import ABC, abstractmethod


class IOutputHandler(ABC):
    def display(self, message: str, separator: str = "\n") -> None: ...


class IStorageBackend(ABC):
    """Abstract storage backend"""

    @abstractmethod
    def read(self) -> list[dict]:
        """Read data from storage"""
        pass

    @abstractmethod
    def write(self, data: list[dict]) -> None:
        """Write data to storage"""
        pass
