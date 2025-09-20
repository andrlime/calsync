import calsync.core.calendar as calendar
import calsync.core.event as event
import calsync.core.output as output
from calsync.util.logger import create_logger

logger = create_logger()


if __name__ == "__main__":
    logger.info("Starting calsync application")

    logger.info("Reading calendar from ICS source")
    ics_calendar_events = calendar.IcsCalendar().read()

    logger.info("Filtering events and generating day buckets")
    filtered_events, filtered_days = event.FilterEvents(ics_calendar_events).filt()

    logger.info("Parsing filtered events")
    parsed_events = event.ParseEvents(filtered_events).filt()

    logger.info("Creating event buckets by day")
    event_buckets = event.BucketEvents(parsed_events, filtered_days).filt()

    logger.info("Writing events to Obsidian files")
    output.ObsidianFileWriter(event_buckets).write()

    logger.info("Calsync application completed successfully")
