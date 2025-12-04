import os
from dotenv import load_dotenv

# ABSOLUTE PATH TO .env (Do NOT change)
ENV_PATH = r"C:\Users\SOMNATH TUPPADA\OneDrive\Desktop\Projects for Companies\twinmind\second mind\backend\.env"

print("Loading .env from:", ENV_PATH)
print("Exists:", os.path.exists(ENV_PATH))

# Load .env file
load_dotenv(dotenv_path=ENV_PATH)

# Debug prints
print("DEBUG PINECONE KEY:", os.getenv("PINECONE_API_KEY"))
print("DEBUG GEMINI KEY:", os.getenv("GEMINI_API_KEY"))  # <-- NEW

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PINECONE
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX")

    # GEMINI (the CORRECT variable name for Gemini Flash 2.5)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    # REMOVE OpenAI unless you use it
    # OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # Chunking settings
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

settings = Settings()
