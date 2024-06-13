from textwrap import dedent

from crewai import Agent, Task


class CompanyTasks:
    """Definition of the tasks of the insight bot"""

    def __init__(self, company_name: str) -> None:
        """Initialize the tasks

        :param str self.company_name: The name on which the tasks are defined
        """
        self.company_name = company_name

    def search_task(self, agent: Agent) -> Task:
        """A task to search relevant source of data for the company

        :param Agent agent: The agent to assign to the task
        :return Task: The created task
        """
        return Task(
            description=dedent(
                f"""
                    Search for relevant websites on Google where we could find accurate and trustworthy information
                    about {self.company_name}. Focus on finding details such as address, phone number, industry
                    division, number of employees, legal ID, and social network links.

                    Guidelines:
                    - Avoid websites that require login such as social networks (e.g., LinkedIn, Facebook), and other
                    platforms that require account creation (e.g., Crunchbase).
                    - Prioritize the following sources:
                    - The company's official website
                    - Legal and regulatory sources (e.g., Infogreffe, EDGAR Search)
                    - Wikipedia
                    - Blogs and reputable news sites
                    - Ensure that the URLs are talking specifically about the same company {self.company_name} and not
                    about other companies with similar names.
                    - Do not use complicate google search, the best search are often the simple ones

                    Company Name: {self.company_name}
                    """
            ),
            expected_output=dedent(
                f"""
                    The output should be a list of the top 5 most relevant URLs that could contain useful company
                    information for {self.company_name}. Each URL should be accompanied by a brief description of why
                    it is considered trustworthy and relevant.
                    """
            ),
            agent=agent,
        )

    def scrape_task(self, agent: Agent) -> Task:
        """A task to scrap and extract relevant company's info from a website

        :param Agent agent: The agent to assign to the task
        :return Task: The created task
        """
        return Task(
            description=dedent(
                f"""
                Scrape the previously identified websites to extract detailed and accurate information
                about {self.company_name}. The data to be gathered should include, but is not limited to:
                - Company name
                - Address
                - Phone number
                - Industry division
                - Number of employees
                - Legal ID
                - Social network links (only publicly available ones, not requiring login)
                - Stock information (if applicable)
                - Other relevant details that provide insight into the company

                Guidelines:
                - Ensure the data is parsed and formatted correctly.
                - Clean the data to remove any irrelevant or duplicate information.
                - Validate the accuracy of the extracted data where possible.
                - Store the extracted data in a structured format such as JSON or CSV.

                Company Name: {self.company_name}
                """
            ),
            expected_output=dedent(
                """
                The output should include the following details in a structured format:
                - Company name
                - Address
                - Phone number
                - Industry division
                - Number of employees
                - Legal ID
                - Social network links
                - Stock information (if applicable)
                - Any other relevant details

                Ensure the data is well-organized and formatted, ready for further processing or analysis.
                """
            ),
            agent=agent,
        )

    def validate_task(self, agent: Agent) -> Task:
        """A task to validate the quality of the retrieved data

        :param Agent agent: The agent to assign to the task
        :return Task: The created task
        """
        return Task(
            description=dedent(
                f"""
                Validate the relevancy, accuracy, and coherence of the data collected for {self.company_name}.
                The validation process should include the following checks:

                - **Weird Data**: Identify and flag any data that appears unusual or out of place, such as unknown
                cities, misspelled names, or other anomalies.
                - **Inconsistent Data**: Ensure all data points are logically consistent. For example, check for
                mismatches like a country listed as France but a city listed as New York, or financial figures that
                do not match the number of employees (e.g., 1B revenue but 0 employees).
                - **Proper Formatting**: Ensure all data is properly formatted, including well-capitalized names,
                no double spaces, no weird characters, and standardized formats for phone numbers, addresses, etc.

                Guidelines:
                - Remove any data that is flagged as inaccurate or inconsistent.
                - Correct minor formatting issues where possible.
                - Ensure the final dataset is clean, consistent, and properly formatted.
                - The output must be only json, nothing more

                Company Name: {self.company_name}
                """
            ),
            expected_output=dedent(
                """
                The output should be the validated data, cleaned of any inaccuracies, inconsistencies, and improperly
                formatted entries. The final dataset should be well-organized and ready for further use. The format
                should be a json format.
                """
            ),
            agent=agent,
        )
