from abc import ABC, abstractmethod

import icalendar


class BaseCalendar(ABC):
    @abstractmethod
    def read(self) -> icalendar.Component:
        """Reads all events from some calendar source"""
        pass
