import os
import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)

class Retriever:
    """
    Handles vector storage and retrieval using FAISS.
    """
    def __init__(self, vector_store_path="vector_store", model="models/embedding-001"):
        self.vector_store_path = vector_store_path
        self.embeddings = GoogleGenerativeAIEmbeddings(model=model)
        self.vector_db = None
        self._load_vector_db()

    def _load_vector_db(self):
        """Loads index from local storage if it exists."""
        if os.path.exists(os.path.join(self.vector_store_path, "index.faiss")):
            try:
                self.vector_db = FAISS.load_local(
                    self.vector_store_path, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
                logger.info("Retriever: Vector database loaded from disk.")
            except Exception as e:
                logger.error(f"Retriever: Failed to load vector db: {e}")

    def create_database(self, chunks):
        """Creates and saves a new FAISS vector database from text chunks."""
        try:
            self.vector_db = FAISS.from_documents(chunks, self.embeddings)
            self.vector_db.save_local(self.vector_store_path)
            logger.info(f"Retriever: Vector database created and saved to {self.vector_store_path}.")
        except Exception as e:
            logger.error(f"Retriever: Failed to create database: {e}")
            raise

    def get_context(self, query, k=3):
        """Retrieves top-k relevant chunks for the query."""
        if not self.vector_db:
            logger.warning("Retriever: Attempted retrieval on empty database.")
            return []
        
        try:
            docs = self.vector_db.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"Retriever: Retrieval error: {e}")
            return []
