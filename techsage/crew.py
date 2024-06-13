import os
from typing import Dict

from crewai import Agent, Crew, Process, Task

from techsage.agents import CompanyAgents
from techsage.llm import llm
from techsage.tasks import CompanyTasks


class CompanyCrew:
    """Definition of the crew of the insight bot"""

    def __init__(self, company_name: str) -> None:
        """Initialize the crew

        :param str company_name: The company name on which should work the crew
        """
        self.company_name = company_name

    def _initialize_agents(self) -> dict:
        """Initiliaze all the agents

        :return dict: The created agents
        """
        agents = CompanyAgents()
        return {
            "searcher": agents.searcher(),
            "scraper": agents.scraper(),
            "validator": agents.validator(),
        }

    def _initialize_tasks(self, agents: Dict[str, Agent]) -> dict:
        """Initiliaze all the tasks

        :param Dict[str, Agent] agents: The availables agents
        :return dict: The created tasks
        """
        tasks = CompanyTasks(self.company_name)
        return {
            "search": tasks.search_task(agents["searcher"]),
            "scraper": tasks.scrape_task(agents["scraper"]),
            "validate": tasks.validate_task(agents["validator"]),
        }

    def _initialize_and_run_crew(self, tasks: Dict[str, Task], agents: Dict[str, Agent]) -> str:
        """Initialize the crew and kick off

        :param Dict[str, Task] tasks: The tasks to do
        :param Dict[str, Agent] agents: The availables agents
        :return str: The result of the kick off
        """
        is_openai_setup = os.environ.get("OPENAI_API_KEY", "") not in ["", "NA"]
        crew = Crew(
            agents=list(agents.values()),
            tasks=list(tasks.values()),
            manager_llm=llm,
            process=Process.sequential,
            cache=True,
            max_rpm=100,
            memory=is_openai_setup,  # True will improve performance but require OpenAI key
            verbose=1,
        )
        result = crew.kickoff(
            {
                "topic": "Data enrichment",
                "quality_standard": "high",
                "goal": "Retrieve public info on a given company",
            }
        )
        return result

    def run(self) -> str:
        """Create the tasks, agents, crew and launch the kick off

        :return str: The result of the kick off
        """
        agents = self._initialize_agents()
        tasks = self._initialize_tasks(agents)
        result = self._initialize_and_run_crew(tasks, agents)
        return result
        return result
