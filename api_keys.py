# api_keys.py
"""
API Keys Configuration for SDIP System
Centralized API key management
"""

import os

# API Keys configuration
API_KEYS = {
    "openai": [
        os.getenv("OPENAI_API_KEY", ""),
    ],
    "anthropic": [
        os.getenv("CLAUDE_API_KEY", ""),
        os.getenv("ANTHROPIC_API_KEY", ""),
    ],
    "google": [
        os.getenv("GOOGLE_API_KEY", ""),
    ]
}

# Filter out empty keys
for provider in API_KEYS:
    API_KEYS[provider] = [key for key in API_KEYS[provider] if key and key.strip()]

# For development/testing - add test keys if no real keys available
if not API_KEYS["openai"]:
    API_KEYS["openai"] = ["test_openai_key"]
    
if not API_KEYS["anthropic"]:
    API_KEYS["anthropic"] = ["test_claude_key"]

print(f"🔑 API Keys loaded:")
for provider, keys in API_KEYS.items():
    print(f"  - {provider}: {len(keys)} key(s) available")
