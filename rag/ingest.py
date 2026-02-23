import os
import logging
from pypdf import PdfReader

# Configure logging
logger = logging.getLogger(__name__)

def load_documents(directory):
    """
    Directly loads documents (PDF, MD, TXT) from a directory 
    without external heavy loaders.
    """
    documents = []
    if not os.path.exists(directory):
        logger.warning(f"Ingest: Directory '{directory}' not found.")
        return documents

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            content = ""
            if filename.endswith(".pdf"):
                reader = PdfReader(filepath)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        content += extracted + "\n"
            elif filename.endswith(".md") or filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                continue
            
            if content.strip():
                documents.append({"text": content, "source": filename})
                logger.info(f"Ingest: Successfully loaded '{filename}'")
        except Exception as e:
            logger.error(f"Ingest: Error loading '{filename}': {e}")
            
    return documents

def get_text_chunks(documents, chunk_size=1000, chunk_overlap=150):
    """
    Lightweight recursive character splitting logic.
    Splits text into manageable chunks while preserving paragraph integrity.
    """
    chunks = []
    for doc in documents:
        text = doc["text"]
        source = doc["source"]
        
        # Simple recursive splitting logic
        start = 0
        while start < len(text):
            end = start + chunk_size
            
            # If not at the end, try to find a nice break point
            if end < len(text):
                # Look for paragraph break, then newline, then space
                for separator in ["\n\n", "\n", " "]:
                    last_sep = text.rfind(separator, start, end)
                    if last_sep != -1 and last_sep > start + (chunk_size // 2):
                        end = last_sep + len(separator)
                        break
            
            chunk_text = text[start:end].strip()
            if len(chunk_text) > 50: # Ignore tiny fragments
                chunks.append({"text": chunk_text, "source": source})
            
            start = end - chunk_overlap
            if start < 0: start = 0 # Safety check
            if end >= len(text): break
            
    logger.info(f"Ingest: Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks
