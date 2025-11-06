from dataclasses import dataclass

import arrow


def create_checkbox_(contents: str, checkbox_type: str = " ") -> str:
    return f"- [{checkbox_type}] {contents}"


def create_location_checkbox_(contents: str) -> str:
    return create_checkbox_(contents, "l")


def create_star_checkbox_(contents: str) -> str:
    return create_checkbox_(contents, "*")


@dataclass
class T:
    rawday: arrow.Arrow
    starttime: str
    endtime: str

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
        location = (
            (
                "\n\t"
                + create_location_checkbox_(f"`at: {self.location.replace('\n', ' ')}`")
            )
            if self.location != ""
            else ""
        )
        organiser = (
            (
                "\n\t"
                + create_star_checkbox_(f"`host: {self.organiser.replace('\n', ' ')}`")
            )
            if self.organiser != ""
            else ""
        )
        return create_checkbox_(f"{str(self)}{location}{organiser}", checkbox_type)
