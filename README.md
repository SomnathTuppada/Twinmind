AI-Powered Second Brain
Intelligent PDF Question-Answering System using Gemini 2.0 Flash + Pinecone + FastAPI

Twinmind is an AI-powered knowledge system that ingests PDFs, chunks and embeds their content, stores them in Pinecone, and enables users to query the documents using natural language.
Built with FastAPI, Gemini Flash, Pinecone, and a lightweight frontend chat UI.

🚀 Features
🔹 AI-Driven PDF Understanding

Upload any PDF (books, notes, reports, research papers)

System extracts text → chunks → embeds using Gemini Embeddings (1536-dim)

Stores semantic vectors in Pinecone

🔹 Chat with Your Documents

Ask natural-language questions

Retrieves relevant chunks from Pinecone

Sends contextual prompt to Gemini Flash 2.0

Returns accurate answers grounded in your documents

🔹 Modern, Fast Backend

Built with FastAPI

CORS enabled for frontend integration

Async and optimized for performance

🔹 Beautiful Minimal Frontend

Simple chat interface (index.html)

PDF upload with progress indicator

Real-time user ↔ AI conversation

Error messages displayed cleanly

🔹 Robust Error Handling

Handles:

Extraction issues

Embedding failures

Rate limits

Empty context cases

Pinecone mismatches

Backend logs show detailed debug info

🔹 Optimized for Speed

Embeds only first 10 meaningful chunks for fast performance

Uses Gemini Embeddings (1536d) compatible with Pinecone index

Added throttling/logging to prevent timeouts

🧠 System Architecture
            ┌─────────────┐
            │   Frontend   │
            │ (index.html) │
            └──────┬──────┘
                   │
                   ▼
        ┌───────────────────────┐
        │        FastAPI         │
        │   /upload/pdf          │
        │   /query               │
        └─────────┬─────────────┘
                  │
   ┌──────────────┴───────────────┐
   │    Backend Processing Flow    │
   │ 1. Extract PDF text           │
   │ 2. Chunk text (N=800, overlap)│
   │ 3. Embed chunks (1536 dims)   │
   │ 4. Store in Pinecone          │
   │ 5. Query: embed → search → LLM│
   └──────────────┬───────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │    Pinecone     │
         │ Vector Database │
         └─────────────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │  Gemini 2.0 Flash     │
       │  (Context QA Engine)  │
       └───────────────────────┘

📁 Project Structure
Twinmind/
│
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI routes
│   │   ├── llm.py            # Gemini Flash wrapper
│   │   ├── embeddings.py     # Gemini embedding logic
│   │   ├── vector_store.py   # Pinecone upsert/query
│   │   ├── pdf_utils.py      # PDF extraction
│   │   ├── config.py         # Env + settings
│   │   └── chunker.py        # Text chunking helpers
│   ├── .env                  # API keys (ignored in Git)
│   └── requirements.txt
│
└── frontend/
    └── index.html             # Chat UI + PDF upload

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/SomnathTuppada/Twinmind.git
cd Twinmind/backend

2️⃣ Create Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate

3️⃣ Install Python Dependencies
pip install -r requirements.txt

4️⃣ Setup .env file

Create backend/.env:

GEMINI_API_KEY=YOUR_GEMINI_KEY
PINECONE_API_KEY=YOUR_PINECONE_KEY
PINECONE_INDEX=second-brain
PINECONE_ENVIRONMENT=us-east-1


(Never push .env to Git!)

5️⃣ Run the Backend
uvicorn app.main:app --reload --port 8000

6️⃣ Run Frontend

Open file:

frontend/index.html


Browser loads chat UI.

💬 Usage
1. Upload a PDF

Click Upload PDF, wait 10–30 seconds.

2. Ask questions

Example:

Summarize the uploaded PDF.

What does the document say about Artificial Intelligence?

3. AI Responds

System extracts context → retrieves chunks → uses Gemini → returns the answer.

🔐 Security Notes

API keys are NOT included in repo

.gitignore protects .env & .venv

All sensitive data is handled on backend

🛠 Tech Stack
Component	Technology
Frontend	HTML, CSS, JavaScript
Backend	FastAPI
Embeddings	Gemini Embedding (1536d)
LLM	Gemini 2.0 Flash
Vector DB	Pinecone
Runtime	Python 3.11
Tools	pdfplumber, pydantic, CORS middleware
🌟 Future Enhancements

Multi-document upload system

Document search & deletion

Streaming AI responses

Chat history saved per user

UI dark/light theme toggle

Deployment on Render/Vercel

🧑‍💻 Author

Somnath Tuppada
Built as part of an AI-powered knowledge assistant system.
GitHub: https://github.com/SomnathTuppada
