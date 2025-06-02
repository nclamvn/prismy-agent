"""
Application settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
TRANSLATION_CACHE_ENABLED = os.getenv("TRANSLATION_CACHE_ENABLED", "true").lower() == "true"
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Create directories
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

print(f"✅ Settings loaded. Provider: {LLM_PROVIDER}")
print(f"✅ OpenAI key: {'Set' if OPENAI_API_KEY else 'Not set'}")
print(f"✅ Anthropic key: {'Set' if ANTHROPIC_API_KEY else 'Not set'}")
