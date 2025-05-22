reporter_agent=FunctionDeclaration(
    name="reporter_agent",
    description="Report the result of a query",
    parameters={
        "type":"object",
        "properties":{
             "query": {
                "type": "string",
                "description":"Your writing still is well known for clear and effective communication.You always summarize long texts into bullet points that contain the most important details."},
            },
        "required":["query"],
    },
)
