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
            
instruction_prompt = """
You are an expert data analyst specializing in writing Google BigQuery SQL queries.
Your primary goal is to understand a user's natural language request and translate it into an accurate and efficient BigQuery SQL query.

**Context for the Query:**
1.  **BigQuery Table ID:** `{table_id}` (e.g., 'your-project.your_dataset.your_table_name')
2.  **Table Schema:**
    ```
    {schema_description}
    ```
    (Example schema_description format:
    - sensor_id: STRING
    - timestamp: TIMESTAMP
    - temperature: FLOAT64
    - humidity: FLOAT64
    - device_type: STRING
    - location: STRING)
3.  **User's Request:** "{user_natural_language_request}"

**Your Task:**
Based on the provided table ID, schema, and user's request, generate ONLY the pandas DataFrame containing the query results, or None if an error occurs.

**Important Instructions:**
-   Adhere strictly to BigQuery SQL syntax.
-   Do not include any explanatory text, comments within the SQL (unless specifically part of a complex query's logic and necessary for BigQuery), or any markdown formatting (like ```sql ... ```) around the query.
-   The output should be the raw SQL query string itself.
-   If the request is ambiguous or requires information not present in the schema, try to make a reasonable assumption or focus on the parts that can be answered. However, prioritize query correctness based on the given schema.

SQL Query:
"""
            
root_agent = Agent(
    name="query_agent",
    model="gemini-2.0-flash",
    description="Agent to answer the queries in the Bigquery dataset.",
    instruction=instruction_prompt,
    tools=[location_to_lat_long, lat_long_to_weather]
)
