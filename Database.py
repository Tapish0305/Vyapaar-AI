from langchain_chroma import Chroma
from chromadb.config import Settings
from typing import List, Optional

def get_chroma_vector_store(
    collection_name: str,
    embedding_fn,
    persist_directory: Optional[str] = None,
    texts: Optional[List[str]] = None,
    metadatas: Optional[List[dict]] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    ssl: bool = False
) -> Chroma:
    """
    Create or load a Chroma vector store.
    Args:
        collection_name (str): Name of the Chroma collection.
        embedding_fn: Embedding function (must implement embed_documents).
        persist_directory (str, optional): Directory to persist/load the collection.
        texts (List[str], optional): List of texts to add (if creating new).
        metadatas (List[dict], optional): Metadata for each text.
        host (str, optional): Chroma server host (for remote DB).
        port (int, optional): Chroma server port.
        ssl (bool, optional): Use SSL for remote connection.
    Returns:
        Chroma: The vector store object.
    """
    # If host/port provided, set up remote client
    client_settings = None
    if host:
        client_settings = Settings(
            chroma_server_host=host,
            chroma_server_http_port=port,
            chroma_server_ssl_enabled=ssl
        )
    
    # If texts provided, create new vector store
    if texts:
        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=embedding_fn,
            metadatas=metadatas,
            collection_name=collection_name,
            persist_directory=persist_directory,
            client_settings=client_settings
        )
    else:
        # Load existing vector store
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_fn,
            persist_directory=persist_directory,
            client_settings=client_settings
        )
    return vector_store