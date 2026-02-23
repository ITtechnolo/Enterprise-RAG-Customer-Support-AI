# Enterprise RAG Bot

A production-ready Enterprise Retrieval-Augmented Generation (RAG) chatbot designed for high reliability and strictly controlled AI responses. This project is built using a modular architecture for scalability and clean separation of concerns.

## 🏗️ Architecture Overview

The system follows a classic RAG pattern, enhanced with semantic chunking and strict prompt engineering to eliminate hallucinations.

### RAG Pipeline Flow:
1. **Ingestion**: Documents (PDF/MD/TXT) are loaded and split into semantic-aware chunks.
2. **Embedding**: Chunks are processed through the Google Gemini Embeddings API.
3. **Storage**: High-dimensional vectors are stored in a local FAISS index.
4. **Retrieval**: User queries are embedded and matched against the top-3 most relevant context chunks.
5. **Generation**: The Gemini-1.5-Flash model generates a response strictly bounded by the retrieved context.

## 🛠️ Tech Stack

- **Python 3.x**: Core logic and RAG pipeline.
- **Flask**: Lightweight web framework for the chat interface.
- **FAISS**: Facebook AI Similarity Search for efficient vector retrieval.
- **LangChain**: Used for document loading and advanced text splitting.
- **Google Gemini API**: state-of-the-art LLM for embeddings and response generation.
- **Numpy**: Vector operations and numerical processing.

## 📦 Project Structure

```text
.
├── app.py              # Flask server and API endpoints
├── rag/                # Core RAG logic package
│    ├── ingest.py      # Document loading and splitting
│    ├── retriever.py   # FAISS vector store management
│    ├── prompt.py      # Strict system prompt definitions
│    └── generator.py   # Gemini API interaction logic
├── vector_store/       # Persistent FAISS indices (Local Storage)
├── knowledge_base/     # Source documents for the AI
├── templates/          # HTML UI templates
└── .env                # Project configuration (Git Ignored)
```

## 🛡️ Anti-Hallucination Features

- **Strict System Prompt**: The AI is explicitly instructed to only use the provided context and respond with a specific fallback if the information is missing.
- **Context Grounding**: By limiting the knowledge source to your local documents, we eliminate the risk of the model using external, outdated, or incorrect training data.
- **Conciseness Injection**: Forcing responses to be under 2 sentences reduces the likelihood of "verbose drifting" into unverified claims.

## 🚀 Installation & Usage

### 1. Prerequisites
- Python 3.9+
- A Google Gemini API Key

### 2. Setup
```bash
# Clone the repository
git clone <repository-url>
cd "Enterprise RAG Customer Support AI"

# Install dependencies
pip install -r requirements.txt
```

### 3. Example Questions to Ask
Test the bot's accuracy and strict policy with these queries:
- **"What is your standard SLA for cloud services?"** (Context: 99.9% uptime)
- **"How long does a refund take?"** (Context: 10 business days)
- **"Is my data encrypted?"** (Context: AES-256 and TLS 1.3)
- **"Who is the CEO of the company?"** (Expected: "I don't have enough information...")

### 4. Persistence & Reliability
This bot is designed to run indefinitely and on any system:
- **Local FAISS Index**: The vector database is saved to the `vector_store/` folder. It persists even if you restart the server days later.
- **Auto-Ingestion**: If you move the project to a new computer, the system will automatically re-index the `knowledge_base/` on the first run.
- **Environment Isolation**: All dependencies are locked in `requirements.txt` for 100% reproducibility.

### 3. Configuration
Rename `.env.example` to `.env` and add your API key:
```env
GEMINI_API_KEY=your_key_here
```

### 4. Running the Bot
```bash
python app.py
```
The server will start at `http://localhost:5000`. On the first run, it will automatically process documents in the `knowledge_base/` folder and create a vector search index.

---
*Developed for high-performance enterprise support environments.*
