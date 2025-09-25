import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain.document_loaders import TextLoader
from typing import List, Optional
from tqdm import tqdm

def load_text_files(
    file_paths: List[str],
    concurrency: int = 1
) -> List:
    """
    Load and process text files, optionally in parallel.
    Args:
        file_paths (List[str]): List of file paths to load.
        concurrency (int): Number of files to process concurrently.
    Returns:
        List[Document]: List of LangChain Document objects.
    """
    def process_file(path):
        try:
            loader = TextLoader(path)
            return loader.load()[0]  # Returns a list; take the first Document
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return None

    docs = []
    if concurrency > 1:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = {executor.submit(process_file, path): path for path in file_paths}
            for future in tqdm(as_completed(futures), total=len(file_paths), desc="Loading files"):
                doc = future.result()
                if doc:
                    docs.append(doc)
    else:
        for path in tqdm(file_paths, desc="Loading files"):
            doc = process_file(path)
            if doc:
                docs.append(doc)
    return docs
