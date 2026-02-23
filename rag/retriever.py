import os
import json
import logging
import numpy as np
from google import genai

logger = logging.getLogger(__name__)

class Retriever:
    """
    A Zero-Dependency Vector Retriever using NumPy and persistent JSON storage.
    Bypasses FAISS and LangChain for maximum environment stability.
    """
    def __init__(self, vector_store_path="vector_store", model="models/gemini-embedding-001"):
        self.vector_store_path = vector_store_path
        self.db_file = os.path.join(vector_store_path, "embeddings_db.json")
        self.model = model
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.data = [] # List of {"text": str, "embedding": list}
        
        if not self.api_key:
            logger.error("Retriever: GEMINI_API_KEY missing.")
            return

        self.client = genai.Client(api_key=self.api_key)
        self._load_database()

    def _load_database(self):
        """Loads the JSON embedding database if it exists."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                logger.info(f"Retriever: Loaded {len(self.data)} chunks from persistent storage.")
            except Exception as e:
                logger.error(f"Retriever: Failed to load database: {e}")

    def _get_embedding(self, text):
        """Generates embedding for a single text chunk."""
        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=text
            )
            return response.embeddings[0].values
        except Exception as e:
            logger.error(f"Retriever: Embedding failed: {e}")
            return None

    def create_database(self, chunks):
        """Generates embeddings for chunks and saves to JSON."""
        if not os.path.exists(self.vector_store_path):
            os.makedirs(self.vector_store_path)

        logger.info(f"Retriever: Generating embeddings for {len(chunks)} chunks...")
        processed_data = []
        for i, chunk in enumerate(chunks):
            text_content = chunk["text"]
            emb = self._get_embedding(text_content)
            if emb:
                processed_data.append({
                    "text": text_content,
                    "source": chunk["source"],
                    "embedding": emb
                })
            
            if (i+1) % 5 == 0:
                logger.info(f"Retriever: Processed {i+1}/{len(chunks)} chunks")

        self.data = processed_data
        try:
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f)
            logger.info(f"Retriever: Database saved successfully to {self.db_file}")
        except Exception as e:
            logger.error(f"Retriever: Failed to save database: {e}")

    def get_context(self, query, k=3):
        """
        Retrieves top-k context chunks using Cosine Similarity via NumPy.
        """
        if not self.data:
            logger.warning("Retriever: Empty database. No context retrieved.")
            return []

        query_emb = self._get_embedding(query)
        if not query_emb:
            return []

        q_vec = np.array(query_emb)
        scores = []

        for item in self.data:
            d_vec = np.array(item["embedding"])
            # Cosine Similarity: (A . B) / (||A|| * ||B||)
            norm_q = np.linalg.norm(q_vec)
            norm_d = np.linalg.norm(d_vec)
            
            if norm_q == 0 or norm_d == 0:
                score = 0
            else:
                score = np.dot(q_vec, d_vec) / (norm_q * norm_d)
            
            scores.append((score, item["text"]))

        # Sort by score descending and return top k
        scores.sort(key=lambda x: x[0], reverse=True)
        results = [text for score, text in scores[:k]]
        logger.info(f"Retriever: Found {len(results)} relevant chunks.")
        return results
