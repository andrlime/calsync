import arrow
import icalendar

import recurring_ical_events  # type: ignore

from calsync.util.config import AppConfig
from calsync.util.logger import create_logger

logger = create_logger()


class FilterEvents:
    def __init__(self, events: icalendar.Component):
        delta = AppConfig().get_config_variable("lookahead_days_inclusive") + 1
        self.begin = arrow.now().floor("day").to("local")
        self.end = self.begin.shift(days=delta)

        self.events = events

    def filt(self) -> list[icalendar.Event]:
        logger.info("Filtered events ok")
        return recurring_ical_events.of(self.events).between(  # type: ignore[no-any-return]
            self.begin.naive, self.end.naive
        )
