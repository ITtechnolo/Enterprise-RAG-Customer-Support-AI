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
enterprise-rag-bot/
├── app.py              # Flask server and API endpoints
├── rag/                # Core RAG logic package
│    ├── ingest.py      # Document loading and splitting
│    ├── retriever.py   # FAISS vector store management
│    ├── prompt.py      # Strict system prompt definitions
│    └── generator.py   # Gemini API interaction logic
├── vector_store/       # Local storage for FAISS indices
├── knowledge_base/     # Source documents for the AI
├── templates/          # HTML UI templates
├── static/             # CSS and JS assets
└── .env                # Project configuration
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
cd enterprise-rag-bot

# Install dependencies
pip install -r requirements.txt
```

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
