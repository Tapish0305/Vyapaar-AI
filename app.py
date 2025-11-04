import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
# Correct imports from smolagents
from smolagents import tool
from smolagents import CodeAgent
from smolagents import InferenceClientModel
from langchain_community.vectorstores import Chroma
from embedding_generators import get_embedding_function
from database_builder import build_and_persist_db
from config import model_name
from google_news import search_google_news
from gst import scrape_gst_rates_tool
from chart_maker import chart_maker
from mudra_website_search import loan_info_tool
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into environment

GST_DATA_URL = 'https://cleartax.in/s/gst-rates'
LOAN_INFO_URL = 'https://www.india.gov.in/pradhan-mantri-mudra-yojna'

@st.cache_resource
def load_retriever():
    db = build_and_persist_db(uploaded_files=None)
    if db is None:
        st.error("Vector database could not be initialized. Check console for errors.")
        return None
    return db.as_retriever(search_kwargs={"k": 5})


def display_chart(response):
    if "error" in response:
        st.error(response.get("error"))
        return

    data = response.get("data")
    if data is None or (isinstance(data, (pd.Series, dict)) and not data):
        st.warning("The AI could not find any data to plot for this query.")
        return

    chart_type = response.get("chart_type")
    fig, ax = plt.subplots()

    if chart_type == "bar":
        df = pd.DataFrame.from_dict(data, orient='index', columns=['value'])
        df.plot(kind='bar', ax=ax, legend=False)
        plt.xticks(rotation=45, ha="right")
    elif chart_type == "pie":
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
    elif chart_type == "line":
        pd.Series(data).plot(kind='line', ax=ax, legend=False)
        plt.axhline(0, color='grey', linewidth=0.8)

    ax.set_title(response.get("title", "Chart"))
    ax.set_xlabel(response.get("x_label", ""))
    ax.set_ylabel(response.get("y_label", ""))
    plt.tight_layout()
    st.pyplot(fig)


# Wrap all tool functions using @tool decorator

@tool
def search_knowledge_base(query: str) -> str:
    """
    Searches the knowledge base with the given query.

    Args:
        query (str): The search query string to send to the knowledge base.

    Returns:
        str: A single string containing all retrieved documents, separated by newlines,
             or an error message if the search fails.
    """
    try:
        retrieved_docs = retriever.invoke(query)
        return "\n\n".join(doc.page_content for doc in retrieved_docs)
    except Exception as e:
        return f"Error: Could not search knowledge base. {e}"

@tool
def chart_maker_wrapper(query: str) -> dict:
    """
    Retrieves documents for a query and then uses them to generate a chart JSON.

    Args:
        query (str): The user query to retrieve documents for and generate the chart.

    Returns:
        dict: A chart JSON specification or a dictionary containing an error message.
    """
    try:
        retrieved_docs_list = retriever.invoke(query)
        retrieved_docs_str = "\n\n".join(doc.page_content for doc in retrieved_docs_list)
        chart_json = chart_maker(query=query, retrieved_docs=retrieved_docs_str)
        return chart_json
    except Exception as e:
        return {"type": "chart", "error": f"Failed to run chart wrapper: {e}"}

# Load retriever once globally
retriever = load_retriever()

# Instantiate the model using the specified model_id
# model_id = "deepseek-ai/DeepSeek-OCR"
# inference_model = InferenceClientModel(model_id=model_id)

# Create the CodeAgent with tools and add_base_tools=True
agent = CodeAgent(
    model=InferenceClientModel(),
    tools=[
        search_knowledge_base,
        chart_maker_wrapper,
        search_google_news,
        scrape_gst_rates_tool,
        loan_info_tool,
    ],
    add_base_tools=True,
)


# Streamlit UI setup
st.title("Vyapaar AI: Smart MSME Support 🚀")
st.info("Ask anything about GST, MSME loans, or ask for data visualizations!")

with st.sidebar:
    # st.header("🔑 API Configuration")

    # # Show input boxes for each API key
    # hf_token_input = st.text_input("HuggingFace Token (HF_TOKEN)", type="password")
    # google_api_input = st.text_input("Google API Key (GOOGLE_API_KEY)", type="password",
    #                                 )
    # openrouter_api_input = st.text_input("OpenRouter API Key (OPENROUTER_API_KEY)", type="password",
    #                                      )

    # # Save button
    # if st.button("💾 Save API Keys"):
    #     os.environ["HF_TOKEN"] = hf_token_input.strip()
    #     os.environ["GOOGLE_API_KEY"] = google_api_input.strip()
    #     os.environ["OPENROUTER_API_KEY"] = openrouter_api_input.strip()

    #     # Also store in session for persistent Streamlit use
    #     st.session_state["HF_TOKEN"] = hf_token_input.strip()
    #     st.session_state["GOOGLE_API_KEY"] = google_api_input.strip()
    #     st.session_state["OPENROUTER_API_KEY"] = openrouter_api_input.strip()

    #     st.success("✅ API keys saved successfully!")
    #     st.rerun()  # Refresh app to apply

    st.header("Admin: Update Knowledge Base")
    uploaded_files = st.file_uploader(
        "Upload new PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
    )
    if st.button("Add to Knowledge Base"):
        if uploaded_files:
            with st.spinner("Processing documents and updating database..."):
                build_and_persist_db(uploaded_files=uploaded_files)
                st.cache_resource.clear()
            st.success("Database updated successfully! The app will reload.")
            st.experimental_rerun()
        else:
            st.warning("Please upload at least one PDF file.")

user_query = st.text_input("Ask your question (e.g., 'What is Mudra loan?' or 'Show me a chart of GST rates')")

if st.button("Get Answer") and user_query.strip():
    if not retriever:
        st.error("Retriever not loaded. Check vector DB connection.")
    else:
        with st.spinner("Thinking... 🤔"):
            try:
                answer = agent.run(user_query)

                st.markdown("---")
                st.markdown("### Detailed Answer")
                if isinstance(answer, dict):
                    # Convert dict to a clean string
                    formatted_answer = "\n\n".join(
                        f"**{k}:** {v.strip()}" for k, v in answer.items()
                    )
                    st.markdown(formatted_answer)
                else:
                    st.write(answer)


                if isinstance(answer, dict) and answer.get("type") == "chart":
                    display_chart(answer)

            except Exception as e:
                st.error("An error occurred while running the agent.")
                st.error(f"Error: {str(e)}")
