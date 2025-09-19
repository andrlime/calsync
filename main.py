import calsync.core.calendar as calendar
import calsync.core.event as event
import calsync.core.output as output


if __name__ == "__main__":
    ics_calendar_events = calendar.IcsCalendar().read()

    filtered_events, filtered_days = event.FilterEvents(ics_calendar_events).filt()
    parsed_events = event.ParseEvents(filtered_events).filt()
    event_buckets = event.BucketEvents(parsed_events, filtered_days).filt()

    output.ObsidianFileWriter(event_buckets).write()
