import os
from typing import Callable, Dict, Optional

from crewai import Agent, Crew, Process, Task

from techsage.agent_core.agents import TechSageAgents
from techsage.agent_core.llm import llm
from techsage.agent_core.tasks import TechSageTasks


class TechSageCrew:
    """Definition of the crew"""

    def __init__(self, topic: str, add_to_chat: Optional[Callable] = None) -> None:
        """Initialize the crew

        :param str topic: The topic on which the crew should work
        :param Optional[Callable] add_to_chat: A method allowing to send message into the app chat, default None
        """
        self.topic = topic
        self.add_to_chat = add_to_chat

    def _initialize_agents(self) -> dict:
        """Initialize all the agents

        :return dict: The created agents
        """
        agents = TechSageAgents(self.add_to_chat)
        return {
            "searcher": agents.searcher(),
            "scraper": agents.scraper(),
            "content_generator": agents.content_generator(),
        }

    def _initialize_tasks(self, agents: Dict[str, Agent]) -> dict:
        """Initialize all the tasks

        :param Dict[str, Agent] agents: The available agents
        :return dict: The created tasks
        """
        tasks = TechSageTasks(self.topic)
        return {
            "search": tasks.search_task(agents["searcher"]),
            "scrape": tasks.scrape_task(agents["scraper"]),
            "generate_content": tasks.generate_content_task(agents["content_generator"]),
        }

    def _initialize_and_run_crew(self, tasks: Dict[str, Task], agents: Dict[str, Agent]) -> str:
        """Initialize the crew and kick off

        :param Dict[str, Task] tasks: The tasks to do
        :param Dict[str, Agent] agents: The available agents
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
                "topic": self.topic,
                "quality_standard": "high",
                "goal": "Retrieve and generate insights on the latest trends in technology, programming, and archi.",
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
