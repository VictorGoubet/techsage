import traceback

import click

import techsage.utils.load_config
from techsage.app import TechSageChatApp
from techsage.crew import TechSageCrew


@click.command()
@click.option(
    "--streamlit",
    "-s",
    default="true",
    help="Set this to True to use streamlit interface, otherwise a shell version will be launched",
)
def launch(streamlit: bool) -> None:
    """Launch the process

    :param bool streamlit: If True the streamlit will be launched, otherwise a shell version will be launched
    """
    if streamlit:
        app = TechSageChatApp()
        app.run()
    else:
        launch_in_shell()


def launch_in_shell() -> None:
    """Launch the process in the shell"""
    try:
        print("\n 👋 Welcome to TechSage Information Gatherer")
        print("---------------------------------------------")
        topic = input("Topic (e.g., Technology, Programming, Architecture):  ")
        techsage_crew = TechSageCrew(topic)
        result = techsage_crew.run()
        print(result)
    except Exception as e:
        print(f" ❌ An error occurred during the search:\n{e}\n{traceback.format_exc()}")
