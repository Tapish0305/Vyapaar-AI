from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from embedding_generators import get_embedding_function
from text_splitter import split_text_into_chunks
import os
import tempfile # To handle temporary files
import shutil # To remove the temp directory

# This directory is now ONLY for building the DB from scratch
PDF_DIR = 'C:/GEN_AI_IBM_competition/OTHER_STUFF' 
PERSIST_DIRECTORY = r'C:/GEN_AI_IBM_competition/vs_code_db'
COLLECTION_NAME = 'langflow'

def build_and_persist_db(uploaded_files = None):
    """
    Builds or loads a Chroma vector database.
    - If it already exists → loads it.
    - If it doesn't exist → builds from scratch using PDFs in PDF_DIR.
    - If uploaded_files are provided → adds them to the existing DB.
    """
    print("🔹 Starting database build/load process...")
    embedding_func = get_embedding_function()

    # --- CASE A: Database exists ---
    if os.path.exists(PERSIST_DIRECTORY):
        print(f"✅ Loading existing database from: {PERSIST_DIRECTORY}")
        db = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embedding_func,
            collection_name=COLLECTION_NAME
        )

        # --- Sub-case: Add new documents from Streamlit upload ---
        if uploaded_files:
            print(f"📄 Adding {len(uploaded_files)} new uploaded file(s) to the database...")
            
            # Create a temporary directory to store uploaded files
            with tempfile.TemporaryDirectory() as temp_dir:
                for uploaded_file in uploaded_files:
                    # Get the path for the file in the temp directory
                    temp_filepath = os.path.join(temp_dir, uploaded_file.name)
                    # Write the file's bytes to that path
                    with open(temp_filepath, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Now, use PyPDFDirectoryLoader on that temp directory
                loader = PyPDFDirectoryLoader(temp_dir, recursive=False)
                documents = loader.load()
                
                if not documents:
                    print("❌ No text could be extracted from the uploaded PDFs.")
                    return db # Return the existing DB

                all_chunks = []
                for doc in documents:
                    chunks = split_text_into_chunks(doc.page_content, chunk_size=1000, chunk_overlap=200, separator="\n")
                    all_chunks.extend(chunks)
                
                print(f"Adding {len(all_chunks)} new chunks to the database.")
                db.add_texts(all_chunks)
                db.persist()
                print("✅ New documents embedded and persisted successfully.")
            # The 'with' block automatically cleans up the temp_dir
        
        return db

    # --- CASE B: Build from scratch (using the hardcoded PDF_DIR) ---
    else:
        print("⚙️ No existing database found. Building from scratch...")
        # This part remains the same, using your original PDF_DIR
        loader = PyPDFDirectoryLoader(PDF_DIR, recursive=False)
        documents = loader.load()
        if not documents:
            print(f"❌ No documents found in the initial PDF_DIR: {PDF_DIR}")
            return None

        all_chunks = []
        for doc in documents:
            chunks = split_text_into_chunks(doc.page_content, chunk_size=1000, chunk_overlap=200, separator="\n")
            all_chunks.extend(chunks)

        print(f"📚 Creating Chroma DB with {len(all_chunks)} chunks...")
        db = Chroma.from_texts(
            texts=all_chunks,
            embedding=embedding_func,
            collection_name=COLLECTION_NAME,
            persist_directory=PERSIST_DIRECTORY
        )
        db.persist()
        print("✅ Database created and saved successfully.")
        return db