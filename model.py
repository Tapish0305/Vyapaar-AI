import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def hf_chat(
    model: str,
    prompt: str,
) -> str:
    """
    Calls a model via the OpenRouter API and returns the response text.

    Args:
        model (str): The model identifier (e.g., 'openai/gpt-4o').
        prompt (str): The user's prompt.
        site_url (str, optional): Your site's URL for OpenRouter rankings.
        site_name (str, optional): Your site's name for OpenRouter rankings.

    Returns:
        str: The content of the model's response.
    """
    # Get the API key from an environment variable named OPENROUTER_API_KEY
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

    # Initialize the OpenAI client to point to the OpenRouter API
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Create the API call, including the extra headers for OpenRouter
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    # Return the text content from the response
    return completion.choices[0].message.content

 