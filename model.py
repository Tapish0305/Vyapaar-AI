import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
def hf_chat(
    model: str,
    prompt: str,
) -> str:
    """
    Call a Hugging Face model via OpenAI-compatible API and return the response text.
    Args:
        model (str): Model name, e.g. 'deepseek-ai/DeepSeek-R1:together' or ':auto'.
        prompt (str): User prompt.
        hf_token (str, optional): Hugging Face API token. If not provided, uses HF_TOKEN env var.
    Returns:
        str: Model response.
    """
    api_key = os.environ.get("HUGGING_FACE_API_KEYS")
    if not api_key:
        raise ValueError("Hugging Face API token is required")

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content