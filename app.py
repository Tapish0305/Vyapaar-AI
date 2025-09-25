# import streamlit as st
# from langchain.document_loaders import PyPDFDirectoryLoader
# from Database import get_chroma_vector_store
# from embedding_generators import get_google_embeddings
# from google_news import search_google_news
# from gst import scrape_gst_rates
# from model import hf_chat
# from prompt_template import PromptTemplate
# from text_splitter import split_text_into_chunks
# from website_crawl import crawl_urls
# import feedparser
# from urllib.parse import quote_plus
# from typing import List, Optional
# import os
# # Import your splitter, embedding, DB, scraper, and template construction functions here

# # === Configuration ===
# PDF_DIR = 'C:\GEN_AI_IBM_competition\OTHER_STUFF'
# COLLECTION_NAME = 'langflow'
# PERSIST_DIRECTORY = r'C:\GEN_AI_IBM_competition\vs_code_db'
# GST_DATA_URL = 'https://cleartax.in/s/gst-rates'
# LOAN_INFO_URL = 'https://www.india.gov.in/pradhan-mantri-mudra-yojna'
# MODEL_NAME = 'Qwen/Qwen3-Next-80B-A3B-Thinking'

# # === Streamlit Interface ===
# st.title("MSME-Sahayak: Smart MSME Support")

# # User input
# user_query = st.text_input("Ask your question about MSME loans, GST, etc.")

# if st.button("Get Answer") and user_query.strip():
#     # 1. Load PDFs and split into chunks
#     with st.spinner("Loading documents..."):
#         loader = PyPDFDirectoryLoader(PDF_DIR, recursive=False)
#         all_documents = loader.load()
#         # Combine pages to a single string (update if you want multi-doc handling)
#         full_text = "\n".join([doc.page_content for doc in all_documents])
#         chunks = split_text_into_chunks(full_text, chunk_size=1000, chunk_overlap=200, separator="\n")

#     # 2. Get embeddings and store in vector DB
#     with st.spinner("Indexing knowledge base..."):
#         embeddings = get_google_embeddings(chunks)
#         database = get_chroma_vector_store(COLLECTION_NAME, embeddings, PERSIST_DIRECTORY)

#     # 3. News & Web scraping
#     with st.spinner("Fetching latest info..."):
#         news = search_google_news(user_query)
#         url_data = scrape_gst_rates(GST_DATA_URL)
#         website_crawl = crawl_urls(LOAN_INFO_URL)

#     # 4. Prepare prompt from template
#     template = """
#     You are an expert AI assistant named "MSME-Sahayak".
#     ## Context from Knowledge Base
#     {context}
#     ---
#     ## web search
#     {web}
#     ---
#     ## Website_url for loan
#     {Website_url}
#     ## Website url for gst
#     {gst_url}
#     ---
#     ---
#     ## User's Question
#     {question}
#     ---
#     ## Your Task
#     Based strictly on the provided context, provide a clear, practical, and step-by-step answer to the user's question.
#     """
#     prompt_template = PromptTemplate(template)
#     prompt = prompt_template.build_prompt(
#         context=database,
#         web=news,
#         Website_url=website_crawl,
#         gst_url=url_data,
#         question=user_query
#     )

#     # 5. Call the LLM (Qwen/Qwen3-Next-80B-A3B-Thinking)
#     with st.spinner("Generating smart answer..."):
#         answer = hf_chat(MODEL_NAME, prompt)

#     # 6. Display result
#     st.markdown("## Answer")
#     st.write(answer)

# st.info("Ask anything related to GST, MSME loans, or government schemes.")

# == Add download, context display, or advanced context visualization if needed ==

import streamlit as st
from langchain_community.vectorstores import Chroma
from embedding_generators import get_embedding_function
from google_news import search_google_news
from gst import scrape_gst_rates
from model import hf_chat
from prompt_template import PromptTemplate
from website_crawl import crawl_urls
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser

# === Configuration ===
PERSIST_DIRECTORY = r'C:\GEN_AI_IBM_competition\vs_code_db'
GST_DATA_URL = 'https://cleartax.in/s/gst-rates'
LOAN_INFO_URL = 'https://www.india.gov.in/pradhan-mantri-mudra-yojna'
MODEL_NAME = 'Qwen/Qwen3-Next-80B-A3B-Thinking'

# Use Streamlit's cache for resource-intensive operations
@st.cache_resource
def load_retriever():
    """
    Loads the retriever from the persisted Chroma database.
    This function is cached so it only runs once per session.
    """
    print("Loading Chroma DB retriever...")
    embedding_func = get_embedding_function()
    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_func
    )
    # The retriever is the interface for searching documents.
    retriever = db.as_retriever(search_kwargs={"k": 5}) # Retrieve top 5 relevant chunks
    print("Retriever loaded successfully.")
    return retriever

def format_docs(docs):
    """Helper function to format retrieved documents into a string."""
    return "\n\n".join(doc.page_content for doc in docs)

# === Streamlit Interface ===
st.title("Vyapaar AI for: Smart MSME Support")
st.info("Ask anything related to GST, MSME loans, or government schemes.")

# Load the retriever once and cache it
retriever = load_retriever()

# User input
user_query = st.text_input("Ask your question about MSME loans, GST, etc.")

if st.button("Get Answer") and user_query.strip():
    with st.spinner("Searching knowledge base and fetching latest info..."):
        # 1. Retrieve relevant context from your static PDF knowledge base (This is now very fast)
        retrieved_docs = retriever.get_relevant_documents(user_query)
        context_from_db = format_docs(retrieved_docs)

        # 2. Fetch dynamic, real-time info from the web
        news = search_google_news(user_query)
        gst_data = scrape_gst_rates(GST_DATA_URL)
        loan_data = crawl_urls(LOAN_INFO_URL)

    # 3. Prepare prompt from template
    template = """
    You are an expert AI assistant named "MSME-Sahayak".
    Your task is to provide a clear, practical, and step-by-step answer to the user's question based strictly on the provided context.
    Also in answer please do not mention about the context provided. Just provide the answer.
    If it is not in the context then generate your best response based on your knowledge.
    ## Context from Knowledge Base (PDFs).
    After you gave the answer then provide the sources you used.
    {context}
    ---
    ## Latest News Search Results
    {web_search}
    ---
    ## Website Data for Loans
    {loan_url_data}
    ---
    ## Website Data for GST
    {gst_url_data}
    ---
    ## User's Question
    {question}
    ---
    ## Final Answer
    """
    prompt_template = PromptTemplate(template)
    prompt = prompt_template.build_prompt(
        context=context_from_db,
        web_search=news,
        loan_url_data=loan_data,
        gst_url_data=gst_data,
        question=user_query
    )

    # 4. Call the LLM
    with st.spinner("Generating smart answer..."):
        answer = hf_chat(MODEL_NAME, prompt)

    # 5. Display result
    st.markdown("---")
    st.markdown("### Answer")
    st.write(answer)

    # (Optional) Display the sources from your database
    with st.expander("Show Retrieved Context from Knowledge Base"):
        st.info(context_from_db)
