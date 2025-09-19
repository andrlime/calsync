import calsync.core.calendar as calendar
import calsync.core.event as event
import calsync.core.duckdb as duckdb
import calsync.core.output as output

from calsync.util.config import AppConfig

if __name__ == "__main__":
    ics_calendar = calendar.IcsCalendar().read()

    all_events = event.IcsReader(ics_calendar).read()
    parsed_events = event.Parser(all_events).parse_and_format()
    filtered_events = duckdb.FilterEvents(parsed_events).filter_by_date()

    output.ObsidianFileWriter(parsed_events).write()
