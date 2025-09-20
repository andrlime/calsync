from dataclasses import dataclass

import arrow


@dataclass
class T:
    # Example: 2025, 10, 20
    year: int
    month: int
    day: int
    rawday: arrow.Arrow

    # Example: 1300, 1445
    starttime: str
    endtime: str

    # Example: Hello world, ABC Field, false
    eventname: str
    location: str
    isimportant: bool

    organiser: str

    def __str__(self) -> str:
        time = (
            f"{self.starttime}-{self.endtime}"
            if self.starttime != self.endtime
            else self.starttime
        )
        return f"{time} {self.eventname}".strip()

    def to_obsidian_string(self) -> str:
        checkbox_type = "!" if self.isimportant else "<"
        location = f"\n\t- [l] `at:{self.location}`" if self.location != "" else ""
        organiser = f"\n\t- [*] `host:{self.organiser}`" if self.organiser != "" else ""
        return f"- [{checkbox_type}] {str(self)}{location}{organiser}"
