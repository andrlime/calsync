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

        logger.info(
            f"Filtering events from {self.begin.format('YYYY-MM-DD')} to {self.end.format('YYYY-MM-DD')} ({delta} days)"
        )
        self.events = events

    def filt(self) -> tuple[list[icalendar.Event], list[arrow.Arrow]]:
        list_of_days = []
        begin = self.begin
        while begin < self.end:
            list_of_days.append(begin)
            begin = begin.shift(days=1)

        filtered_events = recurring_ical_events.of(self.events).between(
            self.begin.naive, self.end.naive
        )

        logger.info(
            f"Event filtering completed: {len(filtered_events)} events found across {len(list_of_days)} days"
        )
        return filtered_events, list_of_days
