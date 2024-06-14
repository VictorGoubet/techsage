import json
import os

from techsage.configure import configure
from techsage.utils.constants import APP_FOLDER


def load_config() -> None:
    """Load the current configuration, define default configuration if something failed"""
    try:
        load_config_file()
    except Exception:
        configure()
        load_config_file()


def load_config_file() -> None:
    """Load the current configuration"""
    config_path = f"{APP_FOLDER}/config.json"
    with open(config_path, "r") as f:
        for k, v in json.load(f).items():
            os.environ[k] = str(v)
