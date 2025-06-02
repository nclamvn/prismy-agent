import os
from dotenv import load_dotenv

print("Checking API key loading...")

# Try different ways to load .env
load_dotenv()
load_dotenv('../../../.env')
load_dotenv('../../.env')
load_dotenv('.env')

api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"API Key found: {'YES' if api_key else 'NO'}")
print(f"Key starts with: {api_key[:10]}..." if api_key else "No key")

# Test IntelligentClaudeCommander directly
from intelligent_claude_commander import IntelligentClaudeCommander
commander = IntelligentClaudeCommander()
print(f"Commander has Claude client: {'YES' if commander.claude else 'NO'}")
