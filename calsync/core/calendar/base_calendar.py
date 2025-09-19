import icalendar

from abc import ABC, abstractmethod


class BaseCalendar(ABC):
    @abstractmethod
    def read(self) -> icalendar.Component:
        """Reads all events from some calendar source"""
        pass
