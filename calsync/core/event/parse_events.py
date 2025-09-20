import arrow
import icalendar

import calsync.core.event as event
from calsync.util.logger import create_logger

logger = create_logger()


class ParseEvents:
    def __init__(self, events: list[icalendar.Event]):
        logger.info(f"Parsing {len(events)} calendar events")
        self.events = [self.parse_event(e) for e in events]
        logger.info(f"Successfully parsed {len(self.events)} events")

    def parse_event(self, e: icalendar.Event) -> event.T:
        event_name = e.get("SUMMARY", "(untitled)")
        dtstart = arrow.get(e.get("DTSTART").dt).to("local")
        dtend = arrow.get(e.get("DTEND").dt).to("local")

        # Hard coded for emails
        organiser = e.get("ORGANIZER", "")
        if organiser != "":
            organiser = organiser.split(":")[1]
            organiser = organiser.split("@")[0]

        return event.T(
            rawday=dtstart,
            starttime=dtstart.format("HHmm"),
            endtime=dtend.format("HHmm"),
            eventname=event_name,
            location=e.get("LOCATION", ""),
            isimportant=("[!]" in event_name),
            organiser=organiser,
        )

    def filt(self) -> list[event.T]:
        logger.info(
            f"Event parsing completed: returning {len(self.events)} parsed events"
        )
        return self.events
