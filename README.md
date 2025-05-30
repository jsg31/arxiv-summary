# ArXiv Paper Fetcher, Ranker, and Reporter

## Project Description

This project automates the process of discovering and summarizing recent AI research papers from ArXiv. It uses a team of AI agents built with CrewAI to handle fetching papers, analyzing their content, and generating a concise HTML report of the top findings for a given day. The AI agents are powered by Google's Gemini model (e.g., `gemini-pro` via CrewAI's LiteLLM integration). The system fetches recent papers from ArXiv, ranks them according to their potential impact and relevance, and generates a comprehensive HTML report summarizing the findings.

### Key Components
*   **`FetchArxivPapersTool`**: A custom CrewAI tool that connects to the ArXiv API to search for and retrieve papers based on selected categories (e.g., `cs.CL`, `cs.AI`) and a specific submission date.
*   **Researcher Agent**: An AI agent responsible for sifting through the fetched papers, evaluating their relevance and significance based on titles and abstracts, and selecting the top 10 papers.
*   **Frontend Engineer Agent**: An AI agent that takes the curated list of papers from the Researcher and formats them into a user-friendly HTML report.

### Workflow
1.  **Input**: The script takes a target date as input (configurable in `app.py`).
2.  **Fetching**: The `FetchArxivPapersTool` retrieves all papers from the specified ArXiv categories submitted on that date.
3.  **Research & Ranking**: The Researcher agent analyzes these papers and compiles a ranked list of the top 10.
4.  **Report Generation**: The Frontend Engineer agent generates an HTML file (`ai_research_report.html`) containing the title, authors, a short summary, and a link for each of the top papers.

## Setup Instructions

To get started, clone the repository and install the required Python packages:
```bash
git clone <repository-url> # Replace <repository-url> with the actual URL
cd <repository-directory> # Replace <repository-directory> with the project's folder name
pip install -r requirements.txt
```

You will also need to set up your environment variables as described below.

The `requirements.txt` file is the primary way to install all necessary Python packages. Key dependencies include `crewai`, `arxiv`, `python-dotenv`, `litellm`, and `google-generativeai`.

These core packages provide the functionalities for:
*   AI agent framework (`crewai`)
*   ArXiv API interaction (`arxiv`)
*   Environment variable management (`python-dotenv`)
*   Interfacing with LLMs like Gemini (`litellm`, `google-generativeai`)

CrewAI uses LiteLLM to connect to various LLMs, including Google Gemini.

### Environment Variables
Create a `.env` file in the root directory of the project and add the following environment variables. This is crucial for the script to authenticate with the Google Gemini API.

    ```env
    GEMINI_API_KEY="your_gemini_api_key_here"

    # Optional: If you are using other services that require API keys, add them here.
    # EXAMPLE_OTHER_SERVICE_API_KEY="your_other_service_key"
    ```
    Replace `"your_gemini_api_key_here"` with your actual Google Cloud API key that has access to the Gemini API.

## Running the Script
Once setup is complete:
1.  Modify the `crew_inputs` dictionary in `app.py` if you want to change the target date for fetching papers.
    ```python
    crew_inputs = {
        "date" : "YYYY-MM-DD" # Change to your desired date
    }
    ```
2.  Run the main script:
    ```bash
    python app.py
    ```

## Output

The script will generate an HTML file named `ai_research_report.html` in the project's root directory. This file contains the ranked list of ArXiv papers and their summaries.
