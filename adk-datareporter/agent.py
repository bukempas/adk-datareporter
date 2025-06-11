import os
import json
import webbrowser
from google.cloud import bigquery
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from .sub_agents import bq_agent
from .sub_agents import reporter_agent

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[bq_agent, reporter_agent]
)