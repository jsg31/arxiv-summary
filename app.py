# Set up environment variables
import os
from dotenv import load_dotenv

"""
This script uses crewAI to define a multi-agent system for fetching,
researching, and reporting on ArXiv papers for a specified date.
It leverages a Gemini model for the AI agents' capabilities.
Users need to set the GEMINI_API_KEY environment variable.
The final output is an HTML report of the top AI research papers.
"""

# Load environment variables from .env file
load_dotenv()

# os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini" # Commented out for Gemini integration

from typing import Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from crewai import Agent, Task, Crew, LLM # Added LLM

import arxiv
import time
import datetime

# Defines the input schema for the Arxiv paper fetching tool.
# Ensures the target_date is provided in the correct format.
class FetchArxivPapersInput(BaseModel):
    """Input schema for FetchArxivPapersTool."""
    target_date: datetime.date = Field(..., description="The specific date for which to fetch ArXiv papers. YYYY-MM-DD format.")

# Defines a custom crewAI tool to fetch papers from ArXiv
# based on specified categories and a target submission date.
class FetchArxivPapersTool(BaseTool):
    """
    A tool to fetch research papers from ArXiv based on specified categories and a target submission date.

    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of what the tool does.
        args_schema (Type[BaseModel]): The Pydantic model defining the input arguments for the tool.
    """
    name: str = "fetch_arxiv_papers"
    description: str = "Fetches all ArXiv papers from selected AI categories (e.g., cs.CL, cs.AI) submitted on the target date."
    args_schema: Type[BaseModel] = FetchArxivPapersInput

    def _run(self, target_date: datetime.date) -> List[dict]:
        """
        Executes the tool to fetch papers from ArXiv.

        Args:
            target_date (datetime.date): The date for which to fetch papers.

        Returns:
            List[dict]: A list of dictionaries, where each dictionary contains details of a fetched paper
                        (title, authors, summary, published date, URL).
        """
        # List of ArXiv categories to search for papers.
        # Example categories: "cs.AI", "cs.LG", "cs.CV", "cs.CL", "cs.MA", "cs.RO"
        # Customize this list based on the desired research areas.
        AI_CATEGORIES = ["cs.CL"] # Example: focusing on Computation and Language

        # Define the date range for the target date (from 00:00:00 to 23:59:59)
        start_date = target_date.strftime('%Y%m%d%H%M')
        end_date = (target_date + datetime.timedelta(days=1)).strftime('%Y%m%d%H%M')

        # Initialize the ArXiv client with pagination and delay settings
        # to respect ArXiv's API rate limits.
        # page_size: Number of results to fetch per request.
        # delay_seconds: Time to wait between requests.
        client = arxiv.Client(
            page_size=100,  # Number of results to fetch per page from the ArXiv API.
            delay_seconds=3  # Time in seconds to wait between consecutive requests to the ArXiv API to respect rate limits.
        )

        all_papers = []

        for category in AI_CATEGORIES:
            print(f"Fetching papers for category: {category}")

            search_query = f"cat:{category} AND submittedDate:[{start_date} TO {end_date}]"

            search = arxiv.Search(
                query=search_query,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                max_results=None  # Fetch all results
            )

            # Collect results for the category
            category_papers = []
            for result in client.results(search):
                category_papers.append({
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'summary': result.summary,
                    'published': result.published,
                    'url': result.entry_id
                })

                # Delay between requests to respect rate limits
                time.sleep(3)

            print(f"Fetched {len(category_papers)} papers from {category}")
            all_papers.extend(category_papers)

        return all_papers

arxiv_search_tool = FetchArxivPapersTool()

# Configure the Gemini LLM
# Make sure to set the GEMINI_API_KEY environment variable.
gemini_llm = LLM(model="gemini/gemini-pro")

# Agent 1: ArXiv Researcher
# This agent is responsible for finding and ranking top research papers
# from the results provided by the FetchArxivPapersTool.
researcher = Agent(
    role = "Senior AI Researcher", # The role of the agent
    goal = "Identify and rank the top 10 most significant ArXiv papers published on {date} in specified AI categories. "
           "Focus on papers with potential for high impact or novel contributions.", # The primary objective of the agent
    backstory = "You are a highly experienced AI researcher with a Ph.D. and numerous publications in top-tier journals and conferences. "
                "You have a keen eye for groundbreaking research and can quickly discern a paper's quality and potential impact from its abstract and title. "
                "Your expertise spans across various AI subfields including NLP, Computer Vision, Machine Learning, and Robotics.", # Background and expertise of the agent
    verbose = True, # Enables detailed logging of the agent's actions
    tools = [arxiv_search_tool], # List of tools the agent can use
    llm=gemini_llm  # Added LLM configuration
)

# Agent 2: Frontend Engineer
# This agent takes the researched papers and compiles them into an
# HTML report.
frontend_engineer = Agent(
    role = "Senior Frontend Engineer specializing in AI Application Interfaces", # The role of the agent
    goal = "Create a well-structured and visually appealing HTML report summarizing the top AI research papers identified by the researcher.", # The primary objective of the agent
    backstory = "You are a seasoned frontend engineer with over a decade of experience in building intuitive and responsive web interfaces. "
                "You have a strong understanding of HTML, CSS, and JavaScript, and you're passionate about making complex information accessible. "
                "You also have a foundational understanding of AI concepts, allowing you to effectively present research findings.", # Background and expertise of the agent
    verbose = True, # Enables detailed logging of the agent's actions
    llm=gemini_llm  # Added LLM configuration
)

# Task for ArXiv Researcher
# Defines the specific task for the researcher agent, including the
# expected input (date) and the desired output format.
research_task = Task(
    description = ("Based on the papers fetched from ArXiv for {date}, identify the top 10 most impactful research papers. "
                   "Consider factors like novelty, methodology, potential applications, and relevance to current AI trends. "
                   "Provide a brief justification for each selection."), # A clear description of the task
    expected_output = (
        "A curated list of the top 10 research papers. Each item in the list should include: "
        "- Paper Title "
        "- List of Authors "
        "- Full Abstract "
        "- Direct URL to the ArXiv paper "
        "- A brief (1-2 sentences) justification for why it's considered a top paper."
    ), # The expected format and content of the task's output
    agent = researcher, # The agent assigned to this task
    human_input = True, # Indicates that this task may require human input or validation during the process
)

# Task for Frontend Engineer
# Defines the task for the frontend engineer to create an HTML report
# based on the research_task's output. Specifies the output file.
reporting_task = Task(
    description = ("Take the curated list of top 10 ArXiv papers and compile them into a user-friendly HTML report. "
                   "The report should be well-organized, easy to read, and visually appealing. "
                   "Each paper entry should include its title (as a clickable link to the ArXiv page), authors, and a concise summary of its abstract (around 2-4 sentences)."), # A clear description of the task
    expected_output = (
        "A single HTML file named 'ai_research_report.html'. "
        "The HTML file should present a list titled 'Top 10 AI Research Papers for {date}'. "
        "Each paper in the list should display: "
        "1. Title (hyperlinked to the ArXiv URL, opening in a new tab). "
        "2. Authors. "
        "3. A concise summary of the abstract (2-4 sentences)."
    ), # The expected format and content of the task's output
    agent = frontend_engineer, # The agent assigned to this task
    context = [research_task], # Specifies that this task depends on the output of the research_task
    output_file = "./ai_research_report.html", # The path where the output HTML file will be saved
    human_input = True, # Indicates that this task may require human input or validation (e.g., reviewing the generated HTML)
)

# Defines the crew, bringing together the agents and their tasks.
# The process will be sequential by default if not specified otherwise.
# Note: 'from crewai import Crew' is already handled by the import 'from crewai import Agent, Task, Crew, LLM'
arxiv_research_crew = Crew(
    agents = [researcher, frontend_engineer],
    tasks = [research_task, reporting_task],
    verbose = True,
)

# Input parameters for the crew kickoff.
# The 'date' will be passed to the tasks that require it.
# Modify 'YYYY-MM-DD' to the desired date for fetching papers.
crew_inputs = {
    "date" : "2025-03-12" # Example target date. Change this to fetch papers for a different date.
}

result = arxiv_research_crew.kickoff(inputs = crew_inputs)
