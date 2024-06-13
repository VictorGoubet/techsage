from crewai import Agent
from llm import llm
from tools import google_search_tool, scrap_website_tool


class CompanyAgents:
    """Definition of all the agents of the insight bot"""

    def searcher(self) -> Agent:
        """An agent dedicated to google search

        :return Agent: The created agent
        """
        return Agent(
            role="Searcher",
            goal="Find relevant sources of information through Google searches.",
            backstory="""
            An experienced internet researcher with a keen eye for relevant sources. You are
            adept at finding accurate and useful information from various online sources.
            """,
            cache=True,
            verbose=1,
            tools=[google_search_tool],
            allow_delegation=False,
            llm=llm,
        )

    def scraper(self) -> Agent:
        """An agent dedicated to website scraping

        :return Agent: The created agent
        """
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
        )

    def validator(self) -> Agent:
        """An agent dedicated to result validation

        :return Agent: The created agent
        """
        return Agent(
            role="Validator",
            goal="Check the relevancy, accuracy, and coherence of the retrieved data.",
            backstory="""
            A meticulous data analyst who ensures the integrity and accuracy of information.
            You are thorough in verifying data consistency and completeness.
            """,
            cache=True,
            verbose=1,
            tools=[],
            allow_delegation=False,
            llm=llm,
        )
