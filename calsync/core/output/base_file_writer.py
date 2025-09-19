from abc import ABC, abstractmethod


class BaseFileWriter(ABC):
    @abstractmethod
    def write(self) -> None:
        """Writes events to some format"""
        pass
