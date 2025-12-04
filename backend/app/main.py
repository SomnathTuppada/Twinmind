from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback
from io import BytesIO  # <-- REQUIRED FIX

from app.config import settings
from app.pdf_utils import extract_text_from_pdf
from app.vector_store import save_chunks_to_pinecone, index
from app.embeddings import embed_batch
from app.llm import ask_gemini


app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# GLOBAL ERROR HANDLER
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print("\nUNHANDLED ERROR:\n", traceback.format_exc())
    return JSONResponse({"error": str(exc)}, status_code=500)


# ---------------------------------------------------------------------------
# SIMPLE HOME CHECK
# ---------------------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Backend running successfully!"}


# ---------------------------------------------------------------------------
# TEST PINECONE ENDPOINT (SAFE)
# ---------------------------------------------------------------------------
@app.get("/test-pinecone")
def test_pinecone():
    try:
        from pinecone import Pinecone

        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        indexes = pc.list_indexes()

        # Convert result to JSON-safe list
        return {"indexes": [str(i) for i in indexes]}

    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# PDF UPLOAD & INGEST
# ---------------------------------------------------------------------------
@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...), user_id: str = "default"):
    try:
        from io import BytesIO

        # Step 1: Read file into memory
        content = await file.read()
        pdf_stream = BytesIO(content)

        # Step 2: Extract text (may return list of dicts, list of strings, or string)
        raw_text = extract_text_from_pdf(pdf_stream)

        # FIX: Normalize PDF output into a single string
        if isinstance(raw_text, list):
            extracted_pages = []

            for item in raw_text:
                if isinstance(item, dict) and "text" in item:
                    extracted_pages.append(item["text"])
                elif isinstance(item, str):
                    extracted_pages.append(item)
                else:
                    raise HTTPException(
                        status_code=500, 
                        detail=f"Unexpected PDF extraction item: {item}"
                    )

            text = "\n".join(extracted_pages)
        else:
            text = raw_text

        # Validate text
        if not isinstance(text, str) or not text.strip():
            raise HTTPException(status_code=400, detail="PDF contains no readable text.")

        # Step 3: Chunk text
        chunks = []
        CHUNK = settings.CHUNK_SIZE
        OVERLAP = settings.CHUNK_OVERLAP

        words = text.split()
        i = 0
        chunk_index = 0

        while i < len(words):
            chunk_words = words[i:i + CHUNK]
            chunk_text = " ".join(chunk_words)

            chunks.append({
                "index": chunk_index,
                "text": chunk_text,
                "page": 1  # placeholder
            })

            chunk_index += 1
            i += CHUNK - OVERLAP

        # Limit chunks to first 10 for faster processing
        max_chunks = min(len(chunks), 10)
        chunks = chunks[:max_chunks]
        
        print(f"DEBUG: PDF created {len(chunks)} chunks (limited to {max_chunks})")

        # Step 4: Store in Pinecone
        source_id = f"{user_id}_{file.filename}"
        print(f"DEBUG: Starting to save {len(chunks)} chunks to Pinecone...")
        save_chunks_to_pinecone(source_id, user_id, chunks)
        print(f"DEBUG: Successfully saved to Pinecone")

        return {"message": "PDF processed", "chunks_stored": len(chunks)}

    except Exception as e:
        print("UPLOAD ERROR:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))




# ---------------------------------------------------------------------------
# QUERY ENDPOINT (RAG)
# ---------------------------------------------------------------------------
@app.post("/query")
async def query_endpoint(payload: dict):
    try:
        query = payload.get("query", "")
        user_id = payload.get("user_id", "default")
        top_k = payload.get("top_k", 5)

        if not query:
            raise HTTPException(status_code=400, detail="Query text missing.")

        # Step 1: Embed user query
        try:
            print(f"DEBUG: Embedding query: {query[:50]}...")
            query_vec = embed_batch([query])[0]
            print(f"DEBUG: Query embedding successful, dimension: {len(query_vec)}")
        except Exception as emb_err:
            print(f"EMBEDDING ERROR: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Embedding failed: {str(emb_err)}")

        # Step 2: Query Pinecone
        try:
            print(f"DEBUG: Querying Pinecone index '{settings.PINECONE_INDEX}' with top_k={top_k}")
            result = index.query(
                vector=query_vec,
                top_k=top_k,
                include_metadata=True
            )
            print(f"DEBUG: Pinecone query returned {len(result.get('matches', []))} matches")
        except Exception as pine_err:
            print(f"PINECONE ERROR: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Pinecone query failed: {str(pine_err)}")

        matches = result.get("matches", [])
        
        # Handle case where no matches are found
        if not matches:
            print("DEBUG: No matches found in Pinecone")
            return {
                "answer": "No relevant documents found in the knowledge base. Please upload documents first.",
                "context_used": [],
                "matches": 0
            }
        
        context_parts = []
        for m in matches:
            meta = m.get("metadata", {}) or {}
            txt = meta.get("text", "")
            if txt:
                context_parts.append(txt)

        full_context = "\n\n".join(context_parts)
        
        if not full_context.strip():
            print("DEBUG: No context text extracted from matches")
            return {
                "answer": "No text content found in matching documents.",
                "context_used": [],
                "matches": len(matches)
            }

        # Step 3: Generate answer from LLM
        try:
            print(f"DEBUG: Calling Gemini with context length: {len(full_context)} chars")
            answer = ask_gemini(full_context, query)
            print(f"DEBUG: Gemini response successful")
        except Exception as llm_err:
            print(f"LLM ERROR: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"LLM generation failed: {str(llm_err)}")

        return {
            "answer": answer,
            "context_used": context_parts,
            "matches": len(matches)
        }

    except HTTPException:
        raise
    except Exception as e:
        print("QUERY ERROR:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
