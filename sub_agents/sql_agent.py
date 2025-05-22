import vertexai
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)
list_dataset = FunctionDeclaration(
    name="list_dataset",
    description="List all datasets in the project",
    parameters={
        "type":"object",
        "properties":{
            "project_id": {"type": "string"},
    },
  },
)
list_tables=FunctionDeclaration(
    name="list_tables",
    description="List all tables in the dataset",
    parameters={
        "type":"object",
        "properties":{
            "dataset_id": {
                "type": "string",
                "description":"The ID of the dataset to list tables from"},
    },
        "required":["dataset_id"],
  }
)
get_table=FunctionDeclaration(
    name="get_table",
    description="Get a table from a dataset",
    parameters={
        "type":"object",
        "properties":{
            "table_id": {
                "type": "string",
                "description":"The ID of the table to get"},
        },
        "required":["table_id"],

    },
)
sql_agent=FunctionDeclaration(
    name="sql_agent",
    description="Get information from data in BigQuery using SQL queries",
    parameters={
        "type":"object",
        "properties":{
               "query": {
                 "type": "string",
                 "description":"SQL query on a single line that will help give quantitative answers to the user's question when run on a BigQuery dataset and table. In the SQL query, always use the fully qualified dataset and table names."},
            },
        "required":["query"],
    },
)
