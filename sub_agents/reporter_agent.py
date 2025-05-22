import google.generativeai as genai
import pandas as pd
from google.adk.agents import Agent
import logging
import requests


def generate_report(self, data: pd.DataFrame):
        """
        Generates a report using Gemini 2.0 based on the provided data.

        Args:
            data: A pandas DataFrame containing the data from the BigQuery agent.

        Returns:
            A string representing the generated report, or None if an error occurs.
        """
        if not self.model:
            print("Gemini model is not initialized. Cannot generate report.")
            return None

        if not isinstance(data, pd.DataFrame):
            print("Invalid data format. Expected a pandas DataFrame.")
            return None

        print("ReporterAgent received data and generating report with Gemini 2.0...")

        try:
            # Convert the pandas DataFrame to a string format, preserving some structure
            # Using to_markdown() can sometimes provide a better structure for LLMs
            data_string = data.to_markdown(index=False)


            # Define the refined prompt for the Gemini model
            prompt = f"""
            Analyze the following data from a BigQuery query and generate a concise and well-structured report.

            The report should include:
            1.  A brief summary of the key findings or overall trends observed in the data.
            2.  Specific insights or notable points extracted from the data. Use bullet points for clarity.
            3.  If applicable, mention any potential anomalies or interesting patterns.
            4.  Present the information clearly and professionally.

            Data:
            {data_string}

            Please format the output as a clear, readable text report.
            """

            # Call the Gemini model to generate the report
            response = self.model.generate_content(prompt)

            # Extract the generated text from the response
            report_text = response.text

            print("Report generated successfully by Gemini 2.0.")
            return report_text

        except Exception as e:
            print(f"Error generating report with Gemini model: {e}")
            return None
            
prompt = f"""Analyze the following data from a BigQuery query and generate a concise and well-structured report.

            The report should include:
            1.  A brief summary of the key findings or overall trends observed in the data.
            2.  Specific insights or notable points extracted from the data. Use bullet points for clarity.
            3.  If applicable, mention any potential anomalies or interesting patterns.
            4.  Present the information clearly and professionally.

            Data:
            {data_string}

            Please format the output as a clear, readable text report.
            """
root_agent = Agent(
    name="reporter_agent",
    model="gemini-2.0-flash",
    description="Agent to make a reporting according to the results of queries.",
    instruction=prompt,
)
