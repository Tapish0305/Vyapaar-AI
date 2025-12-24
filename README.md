# Vyapaar-AI 🏢🤖

### MSME, MUDRA, UDYAM & GST Question Answering Assistant

Vyapaar-AI is an AI-powered assistant built using **LangGraph** and **LangChain** to answer questions related to **MUDRA loans, UDYAM registration, MSME schemes, and GST in India**.
It combines **document-based retrieval** with **real-time web search** to provide accurate and reliable responses.

---

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
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
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
```

> ⚠️ Ensure `.env` is added to `.gitignore`.

---

## ▶️ Run the Application

```bash
streamlit run app.py
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

## 🛣️ Future Enhancements

* Persistent chat history
* Source citation in responses
* Multilingual support (English & Hindi)
* Role-based responses (Business Owner, Student, Accountant)

---

## 📜 License

This project is intended for **educational and research purposes**.

---
