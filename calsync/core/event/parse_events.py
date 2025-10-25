import arrow
import icalendar

import calsync.core.event as event
from calsync.util.logger import create_logger

logger = create_logger()


class ParseEvents:
    def __init__(self, events: list[icalendar.Event]):
        self.events = [pe for e in events if (pe := self.parse_event(e)) is not None]

    def parse_event(self, e: icalendar.Event) -> event.T | None:
        event_name = e.get("SUMMARY", "(untitled)")
        dtstart = arrow.get(e.get("DTSTART").dt).to("local")
        dtend = arrow.get(e.get("DTEND").dt).to("local")

        param_value = e.get("DTSTART").params.get("VALUE", None)

        # Hard coded to ignore all day events
        # TODO: Make more robust
        is_all_day_event = param_value is not None and param_value == "DATE"
        if is_all_day_event:
            return None

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
        logger.info("Parsed events ok")
        return self.events
