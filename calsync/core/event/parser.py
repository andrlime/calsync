import arrow
import icalendar

import calsync.core.event as event


def parse_event(e: icalendar.Event) -> event.T:
    event_name = e.get("SUMMARY", "(untitled)")
    dtstart = arrow.get(e["DTSTART"].dt).to("local")
    dtend = arrow.get(e["DTEND"].dt).to("local")

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
    )
