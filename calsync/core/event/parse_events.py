import arrow
import icalendar

import calsync.core.event as event
from calsync.util.logger import create_logger

logger = create_logger()


class ParseEvents:
    def __init__(self, events: list[icalendar.Event]):
        self.events = [self.parse_event(e) for e in events]
    
    def parse_event(self, e: icalendar.Event) -> event.T:
        event_name = e.get("SUMMARY", "(untitled)")
        dtstart = arrow.get(e["DTSTART"].dt).to("local")
        dtend = arrow.get(e["DTEND"].dt).to("local")
        
        # Hard coded for emails
        organiser = e.get("ORGANIZER", "")
        if organiser != "":
            organiser = organiser.split(":")[1]
            organiser = organiser.split("@")[0]

        return event.T(
            year=dtstart.year,
            month=dtstart.month,
            day=dtstart.day,
            rawday=dtstart,
            starttime=dtstart.format("HHmm"),
            endtime=dtend.format("HHmm"),
            eventname=event_name,
            location=e.get("LOCATION", ""),
            isimportant=("[!]" in event_name),
            organiser=organiser
        )

    def filt(self) -> list[event.T]:
        logger.info("Parsed events ok")
        return self.events
