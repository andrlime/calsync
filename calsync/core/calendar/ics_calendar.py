import icalendar
import requests


from calsync.core.calendar.base_calendar import BaseCalendar
from calsync.util.config import AppConfig
from calsync.util.exceptions import RequestError


class IcsCalendar(BaseCalendar):
    def __init__(self) -> None:
        cfg = AppConfig()
        ics_var_name = cfg.get_config_variable("ics_url_env_variable")
        self.ics_url = cfg.get_environment_variable(ics_var_name)

    def read(self) -> icalendar.Component:
        """Reads all events from some calendar source"""
        try:
            raw_calendar = requests.get(self.ics_url).text
            return icalendar.Calendar.from_ical(raw_calendar)
        except requests.exceptions.RequestException as e:
            raise RequestError("Failed to fetch ICS calendar via GET request") from e
