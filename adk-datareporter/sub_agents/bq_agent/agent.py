import os
import json
import webbrowser
from google.cloud import bigquery
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

def run_bigquery_query(query: str) -> str:
    """
    Executes a read-only query against Google BigQuery and returns the results
    as a JSON string.

    Args:
        query: The SQL query to execute.

    Returns:
        A JSON string representation of the query results.
    """
    try:
        # Prevent queries that might modify data
        if not query.strip().upper().startswith("SELECT") and not query.strip().upper().startswith("WITH"):
            return json.dumps({"error": "Only SELECT queries are allowed."})
            
        client = bigquery.Client(project=GCP_PROJECT_ID)
        query_job = client.query(query)  # Make an API request.
        results = query_job.result()  # Wait for the job to complete.

        # Convert results to a list of dictionaries
        rows = [dict(row) for row in results]
        
        return json.dumps(rows, default=str) # Use default=str to handle non-serializable types like dates
    except Exception as e:
        return json.dumps({"error": f"An error occurred: {e}"})

bq_agent = LlmAgent(
    model="gemini-pro",
    name="bq_agent",
    description="This agent queries Google BigQuery datasets to retrieve data.",
    tools=[run_bigquery_query],
    output_key="bigquery_results"
)