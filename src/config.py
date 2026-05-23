import os

from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Groq API Configuration variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant").strip()
