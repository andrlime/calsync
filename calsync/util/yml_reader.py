"""
Reads stuff from YAML files
"""

from typing import Any

from yaml import load, Loader
from calsync.util.logger import create_logger

logger = create_logger()


def read_yaml_file(path: str) -> dict[str, Any]:
    logger.info(f"Reading YAML file: {path}")
    stream = open(path, "r", encoding="utf-8")
    content = load(stream, Loader)
    stream.close()

    if not isinstance(content, dict):
        logger.error(
            f"YAML file content is not a dictionary: expected dict, got {type(content).__name__}"
        )
        raise TypeError(f"Expected dict, got {type(content).__name__}")

    logger.info(f"Successfully loaded YAML file: {path}")
    return content
