import json
import os

from techsage.utils.constants import APP_FOLDER


def load_config() -> None:
    """Load the current configuration"""
    with open(f"{APP_FOLDER}/config.json", "r") as f:
        for k, v in json.load(f).items():
            os.environ[k] = str(v)


load_config()
