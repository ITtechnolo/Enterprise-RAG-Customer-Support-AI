import os
import logging
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_documents(directory):
    """
    Loads documents from a directory and returns a list of LangChain Documents.
    """
    documents = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
            elif filename.endswith(".md"):
                loader = UnstructuredMarkdownLoader(filepath)
            elif filename.endswith(".txt"):
                loader = TextLoader(filepath)
            else:
                continue
            documents.extend(loader.load())
            logger.info(f"Successfully loaded: {filename}")
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
    return documents

def get_text_chunks(documents):
    """
    Splits documents into semantic-aware chunks using recursive character splitting.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split documents into {len(chunks)} chunks.")
    return chunks
