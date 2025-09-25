# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from typing import List
# import os
# from dotenv import load_dotenv
# load_dotenv()
# def get_embedding_function(texts: List[str], model_name: str = "models/text-embedding-004", batch_size: int = 100, output_dimensionality: int = 768) -> List[List[float]]:
#     api_key = os.environ.get("GOOGLE_API_KEY")
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model=model_name,
#         google_api_key=api_key
#     )
#     """
#     Get embeddings for a list of texts using Google Generative AI Embeddings via LangChain.
#     Args:
#         api_key (str): Your Google API key.
#         texts (List[str]): List of texts to embed.
#         model_name (str): Model name (default: "models/text-embedding-004").
#         batch_size (int): Max batch size (default: 100).
#         output_dimensionality (int): Embedding dimension (default: 768).
#     Returns:
#         List[List[float]]: List of embedding vectors.
#     """
#     return embeddings.embed_documents(
#         texts,
#         batch_size=batch_size,
#         output_dimensionality=output_dimensionality
#     )


from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_embedding_function():
    """
    Initializes and returns the Google Generative AI Embeddings object.
    This is a cleaner way to integrate with LangChain components like ChromaDB.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

    # We return the whole object, so LangChain can use it internally.
    # The model 'models/text-embedding-004' is the default and recommended one.
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key
    )
    return embeddings
