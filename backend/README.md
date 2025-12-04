# Second Brain - Backend (Prototype)

This prototype backend supports:
- PDF uploads (selectable text)
- Text chunking and embedding
- Chroma vector store for retrieval
- Query endpoint that calls Gemini Flash (via google-generativeai client)

## Quick start
1. Create and activate a virtualenv
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set environment variables (example):
   ```bash
   export GOOGLE_API_KEY="YOUR_GOOGLE_KEY"
   export OPENAI_API_KEY="YOUR_OPENAI_KEY"
   export EMBEDDING_PROVIDER="openai"
   ```
3. Run the server:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```
4. Upload a PDF and query via the endpoints.
