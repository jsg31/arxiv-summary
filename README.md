# ArXiv Paper Fetcher, Ranker, and Reporter

## Project Description

This project automates the process of fetching, ranking, and reporting on ArXiv papers. It leverages AI agents to identify relevant and impactful research papers based on user-defined topics. The system fetches recent papers from ArXiv, ranks them according to their potential impact and relevance, and generates a comprehensive HTML report summarizing the findings.

## Key Components

The project is built around a set of specialized AI agents and tools:

*   **`FetchArxivPapersTool`**: This tool is responsible for interacting with the ArXiv API. It fetches the latest papers based on specified search queries or categories.
*   **`Researcher` Agent**: This agent takes the list of papers fetched by `FetchArxivPapersTool` and analyzes them. It reads the abstracts and sometimes the full text to understand the paper's contribution, methodology, and potential impact. It then ranks the papers based on relevance to the user's research interests and overall significance.
*   **`Frontend Engineer` Agent**: This agent takes the ranked list of papers and the researcher's analysis to generate a user-friendly HTML report. The report typically includes summaries of the top papers, links to the original ArXiv entries, and any other pertinent information.

## Setup Instructions

To set up and run this project, you'll need to install the following dependencies:

```bash
pip install crewai arxiv python-dotenv openai
```

These packages provide the core functionalities for the AI agents (`crewai`), ArXiv API interaction (`arxiv`), environment variable management (`python-dotenv`), and accessing OpenAI models (`openai`) if you choose to use them as your backend.

## How to Run the Script

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Assuming you will add a `requirements.txt` file later or instruct the user to use the `pip install` command from the Setup Instructions)*

3.  **Set up Environment Variables:**
    Create a `.env` file in the root directory of the project and add the following environment variables. These are crucial for the script to authenticate with necessary services and configure the AI models.

    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    # Specify the OpenAI model you want to use (e.g., gpt-4, gpt-3.5-turbo)
    OPENAI_MODEL_NAME="gpt-4"

    # Optional: If you are using other services that require API keys, add them here.
    # EXAMPLE_OTHER_SERVICE_API_KEY="your_other_service_key"
    ```
    Replace `"your_openai_api_key_here"` with your actual OpenAI API key.

4.  **Run the main script:**
    *(Assuming the main script is `main.py` or similar. This will need to be adjusted if the entry point script has a different name.)*
    ```bash
    python main.py
    ```

## Output

The script will generate an HTML file named `ai_research_report.html` in the project's root directory. This file contains the ranked list of ArXiv papers and their summaries.
