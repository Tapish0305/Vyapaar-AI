from langchain_text_splitters import CharacterTextSplitter

def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200, separator: str = "\n") -> list[str]:
    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator=separator
    )
    """
    Split text into chunks using LangChain's CharacterTextSplitter.
    Args:
        text (str): The input text to split.
        chunk_size (int): Maximum number of characters per chunk.
        chunk_overlap (int): Number of characters to overlap between chunks.
        separator (str): Character to split on (e.g., '\n', '.', etc.).
    Returns:
        list[str]: List of text chunks.
    """
    return splitter.split_text(text)
