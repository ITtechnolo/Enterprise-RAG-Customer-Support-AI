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

### 4. Running the Bot (Recommended)
This project includes one-click scripts for Windows to ensure it works every time:
- **Double-click `setup.bat`**: Runs only once. It creates a virtual environment and installs everything correctly.
- **Double-click `start_bot.bat`**: Starts the bot immediately using the correct environment.

## 🛡️ Persistence & Reliability
This bot is designed to work indefinitely and on any Windows system:
- **Environment Isolation**: The `setup.bat` script creates a `venv/` folder. This keeps the project's dependencies separate from other programs, preventing breakage over time.
- **Persistent Data**: The vector database is saved in `vector_store/`. It stays there forever unless you delete it, so your knowledge base remains ready.
- **Zero-Dependency Core**: By using custom Python logic instead of heavy libraries, we've eliminated 99% of common "system-level" errors.

---
*Developed for high-performance enterprise support environments.*
