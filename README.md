![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Vyapaar-AI 🏢  
<p align="center">
  <strong>MSME & GST Question Answering Assistant</strong>
</p>

**Vyapaar-AI** is an AI-powered question-answering assistant designed to help users with queries related to **MUDRA loans, UDYAM registration, MSME schemes, and GST in India**.

The system is built using **LangGraph** and **LangChain**, enabling a structured multi-agent workflow. It intelligently combines **document-based retrieval** (GST books, MUDRA documents) with **real-time web search** to deliver accurate, reliable, and up-to-date responses.


## 🚀 Features

* 📌 Answers queries on:

  * MUDRA Loan schemes
  * UDYAM registration
  * GST rules, rates, and compliance
* 🧠 Workflow-driven reasoning using **LangGraph**
* 🔍 Live web search using **Tavily** for current GST and policy updates
* 📚 Retrieval-Augmented Generation (RAG) using:

  * GST reference books
  * Official MUDRA documents
* ⚡ Fast similarity search with **FAISS**
* 🌐 Interactive **Streamlit UI**
* 🔐 Secure API key management via `.env`

---

## 🛠️ Tech Stack

* **LangChain**
* **LangGraph**
* **Google Generative AI (Gemini)**
* **GoogleGenerativeAIEmbeddings**
* **Tavily Search API**
* **FAISS (Vector Database)**
* **Streamlit**

---

## 📁 Project Workflow

```
User Query
   ↓
LangGraph Workflow
   ├── Document Retrieval (GST Books / MUDRA Docs)
   ├── Tavily Web Search (Live GST Updates)
   ↓
LLM Reasoning
   ↓
Final Response
```

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Tapish0305/Vyapaar-AI.git
cd Vyapaar-AI
```

---

### 2. Create Virtual Environment (Recommended)

```bash
conda create -n py39 python=3.9.0
conda activate py39
```

---

### 3. Install Dependencies

```bash
pip install langchain langgraph langchain-core langchain-community langchain-google-genai tavily
pip install faiss-cpu
pip install streamlit
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_generative_ai_key
TAVILY_API_KEY=your_tavily_api_key
HF_TOKEN= your_hf_token
```

## ▶️ Run the Application

```bash
streamlit run streamlit_app.py
```

Open your browser and interact with the chatbot via the Streamlit interface.

---

## 🧠 Embeddings & Retrieval

* **GoogleGenerativeAIEmbeddings** are used to convert documents into vectors
* **FAISS** enables fast and efficient similarity search over GST and MUDRA documents

---

## 🎯 Use Cases

* MSME owners seeking guidance on loans and GST
* Students and researchers exploring Indian financial schemes
* Automated helpdesk for government policy queries

---

## 📜 License

This project is intended for **educational and research purposes**.

---
