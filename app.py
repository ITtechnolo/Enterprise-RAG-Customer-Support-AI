import os
import logging
import warnings

# Suppress irrelevant background dependency warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=UserWarning)

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from rag.ingest import load_documents, get_text_chunks
from rag.retriever import Retriever
from rag.generator import Generator

# Configuration
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EnterpriseBot")

app = Flask(__name__)

# Initialize RAG Pipeline
API_KEY = os.getenv("GEMINI_API_KEY")
KNOWLEDGE_BASE_DIR = "knowledge_base"
VECTOR_STORE_DIR = "vector_store"

retriever = Retriever(vector_store_path=VECTOR_STORE_DIR)
generator = Generator(api_key=API_KEY)

def initialize_kb():
    """Initializes vector store if knowledge base is populated and db is empty."""
    if not os.path.exists(VECTOR_STORE_DIR) or not os.listdir(VECTOR_STORE_DIR):
        logger.info("Initializing knowledge base...")
        docs = load_documents(KNOWLEDGE_BASE_DIR)
        if docs:
            chunks = get_text_chunks(docs)
            retriever.create_database(chunks)
        else:
            logger.warning("No documents found in knowledge base directory.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not API_KEY:
        return jsonify({"response": "System Error: Gemini API Key is missing."}), 500
        
    user_query = request.json.get('message')
    if not user_query:
        return jsonify({"response": "No message provided."}), 400
        
    try:
        # 1. Retrieve
        context = retriever.get_context(user_query, k=3)
        
        # 2. Generate
        response = generator.generate_response(user_query, context)
        
        logger.info(f"Query processed: {user_query}")
        return jsonify({"response": response})
        
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        return jsonify({"response": "An internal error occurred."}), 500

if __name__ == '__main__':
    initialize_kb()
    app.run(debug=True, port=5000)
