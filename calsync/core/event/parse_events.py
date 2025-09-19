import icalendar

import calsync.core.event as event
import calsync.core.event.parser as parser
from calsync.util.logger import create_logger

logger = create_logger()


class ParseEvents:
    def __init__(self, events: list[icalendar.Event]):
        self.events = [parser.parse_event(e) for e in events]

    def filt(self) -> list[event.T]:
        logger.info("Parsed events ok")
        return self.events
