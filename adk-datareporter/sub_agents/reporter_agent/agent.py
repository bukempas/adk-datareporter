import os
import json
import webbrowser
from google.cloud import bigquery
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


reporter_agent = LlmAgent(
    model="gemini-pro",
    name="reporter_agent",
    description="This agent generates HTML reports with charts from JSON data.",
    instruction="""
    You are an expert data visualization developer. You will receive a JSON string
    as input. Your task is to create a comprehensive, single, self-contained HTML 
    report.

    The report MUST include:
    1.  A clear, descriptive title for the report.
    2.  A brief textual summary of the data insights.
    3.  A graphical chart visualizing the data using the Chart.js library. You MUST
        include the Chart.js library from this CDN: 'https://cdn.jsdelivr.net/npm/chart.js'.
    4.  You must analyze the JSON data to determine the most appropriate chart type 
        (e.g., bar, pie, line). For example, use a bar chart for comparing categories, 
        a pie chart for proportions, or a line chart for time-series data.
    5.  The data for the chart (labels and values) must be extracted from the provided JSON.

    Your final output must be ONLY the complete, valid HTML code for the report.
    Do not wrap the code in markdown backticks.
    """
)