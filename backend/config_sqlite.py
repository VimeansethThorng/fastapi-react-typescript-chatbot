import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    # Get the database URL from environment variable, default to "chatbot.db" if not set
    database_url: str = os.getenv("DATABASE_URL", "chatbot.db")

# Create an instance of the Settings class to access configuration variables
settings = Settings()
