from pathlib import Path

from calsync.core.output.base_file_writer import BaseFileWriter
from calsync.util.config import AppConfig

import calsync.core.event as event


class ObsidianFileWriter(BaseFileWriter):
    def __init__(self, events: dict[str, list[event.T]]) -> None:
        cfg = AppConfig()
        self.events = events
        obsidian_env_variable = cfg.get_config_variable("obsidian_env_variable")
        self.base_url = cfg.get_environment_variable(obsidian_env_variable)

        self.start_marker = cfg.get_config_variable("start_marker")
        self.end_marker = cfg.get_config_variable("end_marker")

    def replace_section_(self, path: str, new_text: str) -> None:
        file = Path(path)

        if not file.exists():
            return

        content = file.read_text(encoding="utf-8")
        start = content.find(self.start_marker)
        end = content.find(self.end_marker, start + 1)

        markers_not_found = start == -1 or end == -1
        if markers_not_found:
            return

        updated = (
            content[:start] + self.start_marker + "\n" + new_text + "\n" + content[end:]
        )
        file.write_text(updated, encoding="utf-8")

    def write_day_(self, items: list[event.T]) -> None:
        if len(items) == 0:
            return
        filename = items[0].rawday.format("YY-MMDD-dddd")
        formatted_path = f"{self.base_url}/{filename}.md"

        formatted_items = "\n".join([e.to_obsidian_string() for e in items])
        self.replace_section_(formatted_path, formatted_items)

    def write(self) -> None:
        """Writes files into Obsidian files"""
        for bucket in self.events.values():
            self.write_day_(items=bucket)
