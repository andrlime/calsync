"""
App config singleton class
"""

import os

from typing import Any

from dotenv import load_dotenv

from calsync.util.yml_reader import read_yaml_file
from calsync.util.cli import AppCLI
from calsync.util.logger import create_logger
from calsync.util.exceptions import (
    ConfigValueError,
    CLIValueError,
    EnvironmentValueError,
)

logger = create_logger()


class AppConfig(object):
    """
    Singleton AppConfig class to read config from .env and config.yml and
    return a single dictionary with those values
    """

    def __new__(cls) -> "AppConfig":
        if not hasattr(cls, "instance"):
            cls.instance = super(AppConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if hasattr(self, "config"):
            return

        logger.info("Initializing application configuration")

        cli_instance = AppCLI()
        logger.info("Loading environment variables from .env file")
        load_dotenv()

        config_file = cli_instance.get_parameter_by_key("config")
        logger.info(f"Reading configuration from {config_file}")
        yml_config = read_yaml_file(config_file)

        self.config = {
            "config": yml_config,
            "env": os.environ,
            "cli": cli_instance.get_parameters(),
        }
        logger.info("Application configuration initialized successfully")

    def get_config_variable(self, key: str) -> Any:
        try:
            config = self.config.get("config")
            if config is None:
                logger.error("Config environment doesn't exist")
                raise ConfigValueError("Config environment doesn't exist")
            value_of_key = config.get(key, None)
            if value_of_key is None:
                logger.error(f"Configuration key '{key}' is missing in config file")
                raise ConfigValueError(f"Key {key} missing in config")
            return config.get(key)
        except ValueError as e:
            logger.error(f"Error accessing config variable '{key}': {e}")
            raise ConfigValueError("Config value not found") from e

    def get_cli_argument(self, key: str) -> Any:
        try:
            cli_instance = self.config.get("cli")
            if cli_instance is None:
                raise CLIValueError("CLI environment doesn't exist")
            return cli_instance.get(key, None)
        except ValueError as e:
            raise CLIValueError("CLI value not found") from e

    def get_environment_variable(self, key: str) -> Any:
        try:
            environ = self.config.get("env")
            if environ is None:
                logger.error("ENV environment doesn't exist")
                raise EnvironmentValueError("ENV environment doesn't exist")
            value_of_key = environ.get(key, False)
            if not value_of_key:
                logger.error(f"Environment variable '{key}' is missing or empty")
                raise EnvironmentValueError(f"Key {key} missing in ENV")
            return environ.get(key)
        except ValueError as e:
            logger.error(f"Error accessing environment variable '{key}': {e}")
            raise EnvironmentValueError("Environment variable not found") from e

    def __str__(self) -> str:
        return str(self.config)
