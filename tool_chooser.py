# In your tool_chooser.py file

import ast
from model import hf_chat # Assuming this is your LLM call function
from config import model_name

def choose_tool(user_query: str, tools: list) -> list:
    """
    Chooses the necessary tool(s) to respond to the user's query.
    Returns a list of tool names.
    """
    tool_descriptions = "\n".join([f"- {tool['name']}: {tool['description']}" for tool in tools])

    prompt = f"""
    Given the user's query, identify which of the following tools are necessary to provide a complete answer.
    Respond with a Python list of strings containing the names of the required tools.
    For example, if the chart_maker and text_generator are both needed, respond with: ['chart_maker', 'text_generator']
    If only a text answer is needed, respond with: ['text_generator']

    Available Tools:
    {tool_descriptions}

    User Query: "{user_query}"

    Required Tools (as a Python list):
    """

    try:
        # Call your LLM to get the list of tools
        response = hf_chat(model_name, prompt)
        
        # Safely parse the string representation of the list
        # The model might return "['chart_maker']" as a string
        tool_list = ast.literal_eval(response.strip())

        if isinstance(tool_list, list):
            return tool_list
        else:
            return [] # Return empty list if parsing fails
            
    except (ValueError, SyntaxError):
        # If the LLM returns a malformed list or just plain text, handle it gracefully
        # For a simple fallback, check for keywords
        if "chart" in user_query.lower() or "plot" in user_query.lower():
             return ['chart_maker', 'text_generator'] # Default to both for chart queries
        return ['text_generator'] # Default to text for everything else