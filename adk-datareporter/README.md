# ADK Data Reporter #VertexAISprint

"Google Cloud credits are provided for this project."

## Overview

This project is an AI-powered data reporter that leverages Google's Agent Development Kit (ADK). It allows users to query data from Google BigQuery using natural language and then automatically generates an HTML report with a textual summary and a visual chart based on the retrieved data.

## Features

- **Natural Language Querying:** Utilizes Large Language Models (LLMs) to understand and execute queries against Google BigQuery based on natural language input.
- **Automated Reporting:** Generates comprehensive, self-contained HTML reports from the queried data.
- **Data Visualization:** Automatically creates charts (e.g., bar, pie, line) using Chart.js, selecting the most appropriate chart type for the data.
- **Sequential Processing:** Employs a two-stage pipeline: first retrieving data from BigQuery, then generating a report based on that data.
- **Extensible:** Built with the Google ADK, allowing for customization and extension of agent capabilities.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed and configured:

- Python 3.8 or higher.
- Access to a Google Cloud Platform (GCP) project.
- The BigQuery API enabled in your GCP project.
- Google Cloud SDK installed and initialized.
- Application Default Credentials configured for authentication, typically by running:
  ```bash
  gcloud auth application-default login
  ```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd adk-datareporter
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    The project uses a `dotenv` file to manage environment variables. By default, it's named `dotenv` in the repository.
    *   Make a copy of this file and name it `.env`:
        ```bash
        cp dotenv .env
        ```
    *   Edit the `.env` file and set your Google Cloud Project ID:
        ```
        GCP_PROJECT_ID="your-gcp-project-id"
        ```
        Replace `"your-gcp-project-id"` with your actual GCP project ID.

## Usage

To run the ADK Data Reporter, you can create a Python script or run interactively. Here's an example of how to run the agent using the `Runner` from the Google ADK:

1.  **Create a Python script** (e.g., `run_reporter.py`) in the `adk-datareporter` directory with the following content:

    ```python
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from agent import root_agent # Assuming your main agent instance is root_agent in agent.py
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Ensure GCP_PROJECT_ID is set
    if not os.getenv("GCP_PROJECT_ID"):
        print("Error: GCP_PROJECT_ID environment variable not set.")
        print("Please set it in your .env file.")
        exit(1)

    def main():
        session_service = InMemorySessionService()
        runner = Runner(agent=root_agent, session_service=session_service)

        print("ADK Data Reporter Initialized.")
        print("Enter your data query for BigQuery (e.g., 'What are the total sales per product category last quarter?'):")
        try:
            while True:
                user_input = input("Query > ")
                if user_input.lower() == 'exit':
                    print("Exiting reporter.")
                    break

                response_dict = runner.process_user_input(user_input)

                # The reporter_agent's output is the HTML content
                html_report = response_dict.get("output")

                if html_report:
                    # Save the report to a file
                    report_filename = "report.html"
                    with open(report_filename, "w") as f:
                        f.write(html_report)
                    print(f"Report saved as {report_filename}")
                    # Optionally, open the report in a web browser
                    # import webbrowser
                    # webbrowser.open(report_filename)
                else:
                    print("Could not retrieve report. Response from agent:")
                    print(response_dict)

        except KeyboardInterrupt:
            print("\nExiting reporter.")

    if __name__ == "__main__":
        main()
    ```

2.  **Run the script from your terminal:**
    ```bash
    python run_reporter.py
    ```

3.  **Interact with the agent:**
    *   The script will prompt you to enter your data query for BigQuery.
    *   Type your query and press Enter.
    *   The `bq_agent` will attempt to convert your natural language query into a SQL query and fetch data from BigQuery.
    *   The `reporter_agent` will then take this data and generate an HTML report named `report.html` in the current directory.

**Expected Output:**

An HTML file (e.g., `report.html`) will be created in the `adk-datareporter` directory. This file contains the data summary and a chart visualization. The console will also show the path to this file.

## Agent Architecture

The ADK Data Reporter consists of a main sequential agent that coordinates two sub-agents:

1.  **`bq_agent` (BigQuery Agent):**
    *   **Type:** LLM Agent (`google.adk.agents.LlmAgent`).
    *   **Model:** `gemini-pro`.
    *   **Purpose:** Interprets natural language queries, translates them into SQL queries, and executes them against Google BigQuery.
    *   **Tool:** `run_bigquery_query` - A custom tool that safely executes read-only (`SELECT` or `WITH`) SQL queries and returns results as JSON.
    *   **Output:** The query results are passed in a JSON string format to the next agent under the key `bigquery_results` (though the reporter agent is designed to take the primary output directly).

2.  **`reporter_agent` (Reporter Agent):**
    *   **Type:** LLM Agent (`google.adk.agents.LlmAgent`).
    *   **Model:** `gemini-pro`.
    *   **Purpose:** Takes JSON data (from `bq_agent`) as input and generates a comprehensive, single, self-contained HTML report.
    *   **Functionality:**
        *   Creates a descriptive title for the report.
        *   Provides a brief textual summary of data insights.
        *   Visualizes data using an appropriate chart type (e.g., bar, pie, line) via the Chart.js library (loaded from a CDN).
    *   **Output:** A string containing the complete HTML code for the report.

The `root_agent` in `agent.py` is a `SequentialAgent` that ensures these two sub-agents run in order: data retrieval first, followed by report generation.

## Authentication Note

This application interacts with Google Cloud services (BigQuery) and relies on Application Default Credentials (ADC) for authentication. Ensure that the environment where you run the application has credentials that are authorized to access your BigQuery data.

This typically means:
- You have run `gcloud auth application-default login` in your local environment.
- If running in a Google Cloud environment (like Compute Engine, Cloud Run, etc.), the service account associated with that resource has the necessary IAM permissions for BigQuery (e.g., BigQuery Data Viewer and BigQuery Job User roles at a minimum).

Refer to the [Google Cloud authentication documentation](https://cloud.google.com/docs/authentication/provide-credentials-adc) for more details.


