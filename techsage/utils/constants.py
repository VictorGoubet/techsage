import os

APP_FOLDER = os.path.join(os.path.expanduser("~"), ".techsage")
LIB_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEFAULT_CONFIG = {
    "model": "llama3:8b",
    "model_url": "http://localhost:11434/v1",
    "verbose": 0,
    "local": "true",
    "google_search_api_key": "NA",
    "openai_api_key": "NA",
}
