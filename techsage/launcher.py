import traceback

import techsage.utils.load_config
from techsage.crew import CompanyCrew


def launch() -> None:
    """Launch the process"""
    try:

        print("\n 👋 Welcome to Company Information Gatherer")
        print("---------------------------------------------")
        company_name = input("Company name:  ")
        company_crew = CompanyCrew(company_name)
        result = company_crew.run()
        print(result)
    except Exception as e:
        print(f" ❌ An error occured during the search:\n{e}\n{traceback.format_exc()}")
