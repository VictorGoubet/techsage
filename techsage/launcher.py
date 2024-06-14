import traceback

import techsage.utils.load_config
from techsage.crew import TechSageCrew


def launch() -> None:
    """Launch the process"""
    try:
        print("\n 👋 Welcome to TechSage Information Gatherer")
        print("---------------------------------------------")
        topic = input("Topic (e.g., Technology, Programming, Architecture):  ")
        techsage_crew = TechSageCrew(topic)
        result = techsage_crew.run()
        print(result)
    except Exception as e:
        print(f" ❌ An error occurred during the search:\n{e}\n{traceback.format_exc()}")
