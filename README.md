# 🌐 Translate Export Agent

AI-powered translation and content transformation system with multi-provider support.

## Features
- 🌍 Multi-language translation (8 languages)
- 🤖 Multiple LLM providers (OpenAI GPT-4, Claude 4, Google)
- 🎙️ Content transformation (Podcast, Education, Video)
- 🚀 RESTful API with documentation
- 🎨 Interactive web interface
- 📊 Health monitoring and metrics

## Quick Start
1. Install dependencies: pip install -r requirements.txt
2. Configure environment: Copy .env.example to .env and add API keys
3. Run API: uvicorn src.api.main:app --port 8000
4. Run UI: streamlit run streamlit_ui.py

## Architecture
Clean architecture with separation of concerns:
- Core: Domain logic and interfaces
- Application: Business use cases
- Infrastructure: External integrations
- API: RESTful endpoints
- UI: Streamlit interface
