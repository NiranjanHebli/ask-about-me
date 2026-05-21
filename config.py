import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Azure AI Foundry Configuration variables
AZURE_ENDPOINT = os.getenv("AZURE_FOUNDRY_ENDPOINT", "").strip()
AZURE_API_KEY = os.getenv("AZURE_FOUNDRY_API_KEY", "").strip()
AZURE_MODEL_NAME = os.getenv("AZURE_FOUNDRY_MODEL_NAME", "gpt-4o").strip()
AZURE_AGENT_NAME = os.getenv("AZURE_FOUNDRY_AGENT_NAME", "my-resume-agent").strip()
AZURE_AGENT_VERSION = os.getenv("AZURE_FOUNDRY_AGENT_VERSION", "2").strip()
