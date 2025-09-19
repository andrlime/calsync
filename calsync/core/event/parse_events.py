import icalendar

import calsync.core.event as event
import calsync.core.event.parser as parser


class ParseEvents:
    def __init__(self, events: list[icalendar.Event]):
        self.events = [parser.parse_event(e) for e in events]

    def filt(self) -> list[event.T]:
        return self.events
