import os
import logging
from google import genai
from .prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class Generator:
    """
    Handles text generation using the Gemini API.
    """
    def __init__(self, api_key, model_name="gemini-flash-latest"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate_response(self, query, context_chunks):
        """
        Generates a strictly context-bound response.
        """
        context = "\n---\n".join(context_chunks) if context_chunks else "No relevant context found."
        
        formatted_prompt = SYSTEM_PROMPT.format(context=context, query=query)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=formatted_prompt
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Generator: Response generation failed: {e}")
            return f"Error: Failed to process your request."
