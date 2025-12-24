from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from tavily import TavilyClient
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated
from langchain_core.output_parsers import PydanticOutputParser
import os
from langchain_text_splitters import CharacterTextSplitter
import ast
from langchain_community.vectorstores import FAISS

load_dotenv()

google_api_key = os.environ['GEMINI_API_KEY']
tavily_api_key = os.environ["TAVILY_API_KEY"]

FAISS_PATH = r"G:\My Drive\GEN_AI_IBM_competition\demo_embeddings"

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=google_api_key
)
new_vector_store = FAISS.load_local(
    FAISS_PATH, 
    embeddings, 
    allow_dangerous_deserialization=True
)


retriever = new_vector_store.as_retriever()

client = TavilyClient(api_key=tavily_api_key) 


@tool
def search_knowledge_base(query: str) -> str:

    """
    Retrieve relevant information from the pdf document.
    Use this tool when the user asks about MSME and GST.
    that might be answered from the stored documents.
    """
    result = retriever.invoke(query)

    context = [doc.page_content for doc in result]
    metadata = [doc.metadata for doc in result]

    return {
        'query': query,
        'context': context,
        'metadata': metadata
    }

@tool
def web_search(query: str) -> str:
    """
    This tool answer the query about MSME, GST regulations only in the context of india.
    Args:
        query (str): Search query.
    
    Returns:
        str: Search context or error message.
    """
    response = client.search(
        query=query,
        search_depth="basic",
        max_tokens=2500
    )
    return str(response)

tools = [search_knowledge_base, web_search]


llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3", 
    task="text-generation",
    max_new_tokens=1024,
    do_sample=False,
    repetition_penalty=1.03,
    huggingfacehub_api_token=os.environ['HF_TOKEN']
)

model = ChatHuggingFace(llm=llm)

model_with_tool = model.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    """
    You are a specialized AI assistant for the Department of MSME and GST Council of India. Your sole purpose is to assist users with queries related to Micro, Small, and Medium Enterprises (MSME) and Goods and Services Tax (GST) in India.

### 1. SCOPE OF OPERATIONS
- You must ONLY answer questions directly related to MSME schemes, regulations, registration (Udyam), GST filing, tax slabs, compliance, and government notifications in India.
- If a user asks about topics outside this scope (e.g., general news, entertainment, coding, non-Indian tax laws), strictly REFUSE to answer. State politely that you can only assist with MSME and GST India queries.

### 2. DATA SOURCE PRIORITY
You have access to two information sources: **Provided Context (RAG)** and a **Web Search Tool**. You must follow this strict hierarchy:

**STEP 1: Check Provided Context (RAG)**
- First, analyze the context provided in the user's message or history.
- If the answer is present in the context, generate the response *solely* from that information.
- Do NOT use the Web Search Tool if the Provided Context is sufficient.

**STEP 2: Fallback to Web Search**
- If (and ONLY if) the answer is **not** in the Provided Context, you must evaluate the query:
  - Is the query strictly related to MSME or GST in India?
  - If **YES**: Use the `web_search` tool to find the specific scheme, notification, or regulation.
  - If **NO**: Do not use the tool. Refuse the query as "out of scope."

### 3. RESPONSE GUIDELINES
- **Accuracy:** For GST rates or legal sections, be precise. If the web search is ambiguous, state that you cannot verify the information.
- **Citations:** When using the Web Search tool, mention the source (e.g., "According to the latest CBIC notification...").
- **Tone:** Professional, bureaucratic yet helpful, and strictly objective.

### EXAMPLE BEHAVIORS
- **User:** "How do I register for Udyam?" 
  -> *Action:* Check RAG. If missing, use Web Search for "Udyam registration process India".
- **User:** "What is the GST rate for gold?" 
  -> *Action:* Check RAG. If missing, use Web Search for "current GST rate gold India".
- **User:** "Who won the cricket match yesterday?"
  -> *Action:* IGNORE tools. Reply: "I can only assist with MSME and GST related queries."
    """
    messages = state['messages']
    response = model_with_tool.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")  

chatbot = graph.compile()