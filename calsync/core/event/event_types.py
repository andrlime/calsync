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

    def __str__(self) -> str:
        time = (
            f"{self.starttime}-{self.endtime}"
            if self.starttime != self.endtime
            else self.starttime
        )
        location = f"`{self.location}`" if self.location != "" else ""
        return f"{time} {self.eventname} {location}"

    def to_obsidian_string(self) -> str:
        checkbox_type = "!" if self.isimportant else "<"
        return f"- [{checkbox_type}] {str(self)}"
