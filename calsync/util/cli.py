"""
CLI class that reads specific arguments
"""

from typing import Any, AnyStr
from argparse import Namespace

import argparse
import os
import sys
import pathlib

from calsync.util.exceptions import CLIValueError, PathError
from calsync.util.logger import create_logger

logger = create_logger()


def argv() -> list[str]:
    return sys.argv[1:]


class AppCLI:
    """
    Singleton CLI class to read arguments from an array of strings
    """

    def __new__(cls) -> "AppCLI":
        if not hasattr(cls, "instance"):
            cls.instance = super(AppCLI, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if hasattr(self, "args"):
            return

        logger.info("Parsing command line arguments")
        arguments = argv()

        parser = argparse.ArgumentParser(
            prog="calsync",
            description="""
Syncs from an ICS format calendar and streams to some other destination
            """,
        )

        parser.add_argument(
            "-c",
            "--config",
            help="Path to config.yml/config.yaml file",
            type=pathlib.Path,
            required=True,
        )

        self.args = parser.parse_args(arguments)
        logger.info(f"Parsed CLI arguments: config file = {self.args.config}")
        self.lint()

    def lint(self) -> None:
        arguments: Namespace = self.args

        if not os.path.isfile(arguments.config):
            logger.error(f"Invalid config file: {arguments.config}")
            raise PathError(f"Invalid config file {arguments.config}")

        logger.info("CLI argument validation completed successfully")

    def get_parameters(self) -> dict[str, Any]:
        return dict(vars(self.args))

    def get_parameter_by_key(self, key: AnyStr) -> str:
        try:
            key_str = str(key)
            return str(vars(self.args)[key_str])
        except ValueError as e:
            raise CLIValueError(f"CLI does not contain key {str(key)}") from e

    def get_path_by_key(self, key: AnyStr) -> str:
        path = self.get_parameter_by_key(key)
        return os.path.abspath(path)
