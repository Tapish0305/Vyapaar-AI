from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from embedding_generators import get_embedding_function
from text_splitter import split_text_into_chunks
import os
import shutil

PDF_DIR = 'C:/GEN_AI_IBM_competition/OTHER_STUFF'
PERSIST_DIRECTORY = r'C:/GEN_AI_IBM_competition/vs_code_db'
COLLECTION_NAME = 'langflow'

def build_and_persist_db():
    """
    This function builds the vector database from PDF files and saves it to disk.
    Run this script once to set up your database.
    """
    print("Starting database build process...")
    embedding_func = get_embedding_function()
    if os.path.exists(PERSIST_DIRECTORY):
        # --- A. LOAD THE EXISTING DATABASE ---
        print(f"Loading existing database from: {PERSIST_DIRECTORY}")
        db = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embedding_func,
            collection_name=COLLECTION_NAME
        )
        print("Database loaded successfully.")
        return db

    else:
        # --- B. CREATE A NEW DATABASE FROM SCRATCH ---
        print("No existing database found. Building a new one...")   
        # 1. Load PDFs
        print(f"Loading documents from: {PDF_DIR}")
        loader = PyPDFDirectoryLoader(PDF_DIR, recursive=False)
        documents = loader.load()
        if not documents:
            print("No documents found.")
            return
        print(f"Loaded {len(documents)} document pages.")

        # 2. Split documents into chunks
        all_chunks = []
        for doc in documents:
            chunks = split_text_into_chunks(doc.page_content, chunk_size=1000, chunk_overlap=200, separator="\n")
            for chunk in chunks:
                all_chunks.append(chunk)

        print(f"Split documents into {len(all_chunks)} chunks.")

        # 3. Create and persist the Chroma database
        print(f"Creating Chroma database at: {PERSIST_DIRECTORY}")
        db = Chroma.from_texts(
            texts=all_chunks,
            embedding=embedding_func,
            collection_name=COLLECTION_NAME,
            persist_directory=PERSIST_DIRECTORY
        )
        print("Database built and persisted successfully!")
        return db
