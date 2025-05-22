from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from datareporter.sub_agents.sql_agent import root_agent as query_agent
from datareporter.sub_agents.reporter_agent import root_agent as reporter_agent


    def run_report(self, query: str):
        """
        Orchestrates the process of getting data and generating the report.

        Args:
            query: The SQL query to execute.
        """
        if not self.bigquery_agent or not self.reporter_agent:
            print("Sub-agents are not set. Cannot run report.")
            return None

        print(f"Running report with query: {query}")

        # Step 1: Get data from BigQuery (placeholder)
        print("Calling BigQuery sub-agent to get data...")
        # data = self.bigquery_agent.get_data(query) # Uncomment when sub-agent is implemented
        data = f"Placeholder data for query: {query}" # Placeholder

        if not data:
            print("Failed to get data from BigQuery.")
            return None

        # Step 2: Generate report using the reporter agent (placeholder)
        print("Calling reporter sub-agent to generate report...")
        # report = self.reporter_agent.generate_report(data) # Uncomment when sub-agent is implemented
        report = f"Placeholder report based on data: {data}" # Placeholder

        if not report:
            print("Failed to generate report.")
            return None

        # Step 3: Present the final output
        print("\n--- Final Report ---")
        print(report)
        print("--------------------")

        return report
prompt=""" You are an insightful data analyst tasked with explaining data findings in a clear, concise, and human-readable report.

**Context:**
1.  **Original User Question/Request:** "{original_user_request}"
    (This was the initial question that led to the data being queried.)

2.  **Data from the Query (e.g., from BigQuery, SQL database, etc.):**
    ```
    {query_results_data}
    ```
    (This data is the direct output from the executed query. It could be in a format like a list of dictionaries, CSV-like string, or a simple tabular string representation.)

**Your Task:**
Based on the original user question and the provided query results, generate a comprehensive yet easy-to-understand report.

**Report Guidelines:**
-   **Directly Address the User's Question:** Ensure the report clearly answers or addresses the `{original_user_request}`.
-   **Summarize Key Findings:** Highlight the most important insights, trends, or answers found in the `{query_results_data}`.
-   **Use Clear Language:** Avoid jargon where possible, or explain it if necessary. The report is for a general audience unless the original request implies a technical one.
-   **Structure (Optional but Recommended):** Consider using:
    * A brief introductory sentence.
    * Bullet points for key findings if appropriate.
    * A concluding summary.
-   **Tone:** Professional, informative, and helpful.
-   **Focus on the Data:** Base your report strictly on the provided `{query_results_data}`. Do not invent information or make assumptions beyond what the data supports in relation to the user's request.
-   **Conciseness:** Be thorough but avoid unnecessary verbosity.

**Output Format:**
Produce plain text suitable for direct display to a user. Do not include any special formatting like Markdown (e.g., ```) unless it's naturally part of the report's content (like a list).

**Generated Report:**
"""

root_agent = Agent(
    name="datareporter_agent",
    model="gemini-2.0-flash",
    description="Making a report of data analysis in a Bigquery dataset according to the queries",
    instruction=prompt,
    # sub_agents=[query_agent, reporter_agent]
    tools=[
        AgentTool(agent=query_agent),
        AgentTool(agent=reporter_agent),]
)
