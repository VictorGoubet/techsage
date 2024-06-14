from textwrap import dedent

from crewai import Agent, Task


class TechSageTasks:
    """Definition of the tasks of the insight bot"""

    def __init__(self, topic: str) -> None:
        """Initialize the tasks

        :param str topic: The topic on which the tasks are defined
        """
        self.topic = topic

    def search_task(self, agent: Agent) -> Task:
        """A task to search relevant sources of data for the topic

        :param Agent agent: The agent to assign to the task
        :return Task: The created task
        """
        return Task(
            description=dedent(
                f"""
                    Search for relevant websites and sources on Google where we could find
                    accurate and trustworthy information about {self.topic}. Focus on finding
                    the latest trends, news, and in-depth articles on technology, programming,
                    and architecture.

                    Guidelines:
                    - Do not use special Google search keywords like 'site:', 'inurl:', 'intitle:', etc.
                    - Use simple and direct search queries. For example: "sagemaker tutorial",
                    "latest trends in AI", "Python programming tips".
                    - Prioritize the following sources:
                    - Reputable tech news websites
                    - Official company blogs and technical reports
                    - Academic journals and publications
                    - Developer community forums (e.g., Stack Overflow, GitHub Discussions)
                    - Ensure that the URLs are specifically about the topic {self.topic}.

                    Topic: {self.topic}
                    """
            ),
            expected_output=dedent(
                f"""
                    The output should be a list of the top 5 most relevant URLs that could contain
                    useful information for {self.topic}. Each URL should be accompanied by a brief
                    description of why it is considered trustworthy and relevant.
                    """
            ),
            agent=agent,
        )

    def scrape_task(self, agent: Agent) -> Task:
        """A task to scrap and extract relevant info from identified websites

        :param Agent agent: The agent to assign to the task
        :return Task: The created task
        """
        return Task(
            description=dedent(
                f"""
                Scrape the previously identified websites to extract detailed and accurate information
                about {self.topic}. The data to be gathered should include, but is not limited to:
                - Latest news and trends
                - In-depth articles
                - Technical reports
                - Community discussions
                - Academic papers

                Guidelines:
                - Ensure the data is parsed and formatted correctly.
                - Clean the data to remove any irrelevant or duplicate information.
                - Validate the accuracy of the extracted data where possible.
                - Store the extracted data in a structured format such as JSON or CSV.

                Topic: {self.topic}
                """
            ),
            expected_output=dedent(
                """
                The output should include the following details in a structured format:
                - Latest news and trends
                - In-depth articles
                - Technical reports
                - Community discussions
                - Academic papers

                Ensure the data is well-organized and formatted, ready for further processing or analysis.
                """
            ),
            agent=agent,
        )

    def generate_content_task(self, agent: Agent) -> Task:
        """A task to generate insightful content based on collected data

        :param Agent agent: The agent to assign to the task
        :return Task: The created task
        """
        return Task(
            description=dedent(
                f"""
                Generate an insightful article or report based on the latest trends and
                information about {self.topic}. The content should be engaging, informative,
                and useful for readers interested in technology, programming, and architecture.

                Guidelines:
                - Provide a compelling introduction to the topic.
                - Summarize key trends and insights.
                - Include relevant examples and case studies.
                - Ensure the content is well-structured and easy to read.

                Topic: {self.topic}
                """
            ),
            expected_output=dedent(
                """
                The output should be a well-written article or report that includes:
                - An engaging introduction
                - Summary of key trends and insights
                - Relevant examples and case studies
                - A concluding summary

                Ensure the content is ready for publication or further distribution.
                """
            ),
            agent=agent,
        )
