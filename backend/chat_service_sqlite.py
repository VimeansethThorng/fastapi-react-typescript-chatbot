from openai import OpenAI
from config_sqlite import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        try:
            # Simple initialization without extra parameters
            self.client = OpenAI(
                api_key=settings.openai_api_key
            )
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {e}")
            raise e
        
    async def generate_response(self, messages: list) -> str:
        try:
            # Enhanced system prompt with LaTeX and markdown instructions
            system_prompt = """You are a helpful assistant chatbot.
            * using write equation using $$$$


            """

            # Format messages for OpenAI API
            formatted_messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            for row in messages:
                role, content = row[0], row[1]  # SQLite returns tuples
                formatted_messages.append({"role": role, "content": content})
            
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=formatted_messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error while processing your request."

chat_service = ChatService()
