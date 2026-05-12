import anthropic
from config_sqlite import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        try:
            self.client = anthropic.AsyncAnthropic(
                api_key=settings.anthropic_api_key
            )
        except Exception as e:
            logger.error(f"Error initializing Anthropic client: {e}")
            raise e

    async def generate_response(self, messages: list) -> str:
        try:
            system_prompt = (
                "You are a helpful assistant chatbot. "
                "Write mathematical equations using LaTeX syntax with $ delimiters "
                "(e.g., $E = mc^2$ for inline, $$F = ma$$ for block equations)."
            )

            formatted_messages = []
            for row in messages:
                role, content = row[0], row[1]  # SQLite returns tuples
                formatted_messages.append({"role": role, "content": content})

            response = await self.client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=1024,
                system=[{
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }],
                messages=formatted_messages,
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error while processing your request."

chat_service = ChatService()
