import json
import os
import traceback

from crew import CompanyCrew


def load_config() -> None:
    """Load the current configuration"""
    with open("./config.json", "r") as f:
        for k, v in json.load(f):
            os.environ[k] = v


def launch() -> None:
    """Launch the process"""
    try:
        load_config()
        print("\n 👋 Welcome to Company Information Gatherer")
        print("---------------------------------------------")
        company_name = input("Company name:  ")
        company_crew = CompanyCrew(company_name)
        result = company_crew.run()
        print(result)
    except Exception as e:
        print(f" ❌ An error occured during the search:\n{e}\n{traceback.format_exc()}")
        print(f" ❌ An error occured during the search:\n{e}\n{traceback.format_exc()}")
