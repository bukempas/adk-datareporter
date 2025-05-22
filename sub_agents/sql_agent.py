import os
from google.adk.code_executors import VertexAiCodeExecutor
from google.adk.agents import Agent

    def get_data(self, query: str):
        """
        Connects to BigQuery, executes a query, and retrieves the results.

        Args:
            query: The SQL query string to execute.

        Returns:
            A pandas DataFrame containing the query results, or None if an error occurs.
        """
        if not self.client:
            print("BigQuery client is not initialized. Cannot get data.")
            return None

        print(f"BigQueryAgent executing query: {query}")

        try:
            # Execute the query
            query_job = self.client.query(query)

            # Wait for the job to complete and get the results
            results = query_job.result()

            # Convert the results to a pandas DataFrame
            dataframe = results.to_dataframe()

            print("Data retrieved successfully from BigQuery.")
            return dataframe

        except Exception as e:
            print(f"Error executing BigQuery query or retrieving data: {e}")
            return None
            
root_agent = Agent(
    name="query_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questionswith queries in the Bigquery dataset .",
    instruction=instruction_prompt,
    tools=[location_to_lat_long, lat_long_to_weather]
)
