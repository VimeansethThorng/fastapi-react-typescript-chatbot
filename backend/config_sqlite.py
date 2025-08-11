import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    database_url: str = os.getenv("DATABASE_URL", "chatbot.db")

settings = Settings()
