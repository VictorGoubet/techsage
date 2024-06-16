from typing import Callable, List, Optional, Tuple

from crewai import Agent
from crewai.agent import AgentAction

from techsage.agent_core.llm import llm
from techsage.agent_core.tools import google_search_tool, scrap_website_tool


class TechSageAgents:
    """Definition of all the agents"""

    def __init__(self, add_to_chat: Optional[Callable]) -> None:
        """Initialize the techsage agents

        :param Optional[Callable] add_to_chat: A method allowing to send message into the app chat
        """
        self.add_to_chat = add_to_chat

    def _step_call_back(self, actions: List[Tuple], agent_name: str, avatar: str) -> None:
        """A method called after each step for logging purposes.

        :param List[Tuple] actions: The actions output of the step.
        :param str agent_name: The name of the agent performing this step.
        :param str avatar: The avatar to use in the chat.
        """
        if not self.add_to_chat:
            return

        msg = [self._format_action(a) for a in actions]
        self.add_to_chat("\n\n".join(msg), agent_name, avatar)

    def _format_action(self, action: Tuple) -> str:
        """Format a single action into a string message.

        :param Tuple action: A single action tuple.
        :return: The formatted action message.
        :rtype: str
        """
        if action[0] == "return_values":
            return f"```\n{action[1]['output']}\n```"
        elif action[0] == "log":
            return action[1]
        elif isinstance(action[0], AgentAction):
            return self._format_agent_action(action)
        return ""

    def _format_agent_action(self, action: Tuple) -> str:
        """Format an AgentAction into a string message.

        :param Tuple action: A single AgentAction tuple.
        :return: The formatted AgentAction message.
        :rtype: str
        """
        action_dict, output = dict(action[0]), action[1]
        action_msg = action_dict.get("log", "")
        if action_dict.get("tool"):
            tool_input = action_dict["tool_input"].replace("\n", " ")
            action_msg += f"\n - **Tool** : `{action_dict['tool']}`\n - **Tool Input** : `{tool_input}`\n"
        action_msg += f"\n**Output** :\n\n```\n{output}\n```"
        return action_msg

    def searcher(self) -> Agent:
        """An agent dedicated to webssearch

        :return Agent: The created agent
        """
        role, avatar = "Searcher", "🧐"
        return Agent(
            role=role,
            goal="Find relevant sources of information through web searches on technology,\
            programming, and cloud architecture.",
            backstory="""
            An experienced internet researcher with a keen eye for relevant sources. You are
            adept at finding accurate and useful information from various online sources.
            """,
            cache=True,
            verbose=1,
            tools=[google_search_tool],
            allow_delegation=False,
            llm=llm,
            step_callback=lambda x: self._step_call_back(x, role, avatar),
        )

    def scraper(self) -> Agent:
        """An agent dedicated to website scraping

        :return Agent: The created agent
        """
        role, avatar = "Scraper", "🕷️"
        return Agent(
            role="Scraper",
            goal="Scrape the content of identified websites to extract useful information.",
            backstory="""
            A skilled web scraper with a background in data extraction. You are proficient in
            parsing and cleaning data to ensure accuracy.
            """,
            cache=True,
            verbose=1,
            tools=[scrap_website_tool],
            allow_delegation=False,
            llm=llm,
            step_callback=lambda x: self._step_call_back(x, role, avatar),
        )

    def content_generator(self) -> Agent:
        """An agent dedicated to generating insightful content

        :return Agent: The created agent
        """
        role, avatar = "Content Generator", "✏️"
        return Agent(
            role="Content Generator",
            goal="Generate insightful content based on the latest trends and information.",
            backstory="""
            A creative and knowledgeable content creator who excels at producing engaging and\
            informative articles and reports.
            """,
            cache=True,
            verbose=1,
            tools=[],
            allow_delegation=False,
            llm=llm,
            step_callback=lambda x: self._step_call_back(x, role, avatar),
        )
