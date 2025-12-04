# backend/app/embeddings.py
import google.generativeai as genai
from app.config import settings
import time

# ensure key is configured
genai.configure(api_key=settings.GEMINI_API_KEY)

# Primary (recommended) embedding model for Gemini
EMBED_MODEL = "gemini-embedding-001"
TARGET_DIM = 1536  # must match your Pinecone index

def embed_batch(texts):
    """
    Generate embeddings for a batch of input texts using Gemini embeddings.
    Ensures the returned embeddings have dimension TARGET_DIM (1536).
    Returns: list[list[float]]
    """

    if not isinstance(texts, list):
        texts = [texts]

    embeddings = []

    for idx, text in enumerate(texts):
        print(f"DEBUG: Embedding text {idx+1}/{len(texts)} (length: {len(text)} chars)")
        
        # Try the simple helper first (some genai versions expose this)
        try:
            # Attempt: genai.embed_content(...)
            print(f"  Calling genai.embed_content()...")
            resp = genai.embed_content(
                model=EMBED_MODEL,
                content=text,
                task_type="retrieval_document",
                output_dimensionality=TARGET_DIM  # request 1536 dims
            )
            vec = resp["embedding"] if isinstance(resp, dict) else resp.embedding
            print(f"  OK - Got embedding dimension {len(vec)}")
        except Exception as e1:
            print(f"  FAILED - First method: {str(e1)[:100]}")
            # Fallback: client-style call genai.models.embed_content(...)
            try:
                print(f"  Trying fallback method: genai.models.embed_content()...")
                resp2 = genai.models.embed_content(
                    model=EMBED_MODEL,
                    contents=[text],
                    output_dimensionality=TARGET_DIM
                )
                # resp2 may expose .embeddings or ['embeddings']
                if hasattr(resp2, "embeddings"):
                    vec = resp2.embeddings[0]
                elif isinstance(resp2, dict) and "embeddings" in resp2:
                    vec = resp2["embeddings"][0]
                elif isinstance(resp2, dict) and "embedding" in resp2:
                    vec = resp2["embedding"]
                else:
                    raise RuntimeError(f"Unexpected embedding response format: {type(resp2)}")
                print(f"  OK - Fallback success! Got embedding dimension {len(vec)}")
            except Exception as e2:
                # Surface a clear error so we can debug in logs
                error_msg = f"Embedding failed for text chunk {idx+1}. Errors: {str(e1)[:100]} | {str(e2)[:100]}"
                print(f"  FAILED - {error_msg}")
                raise RuntimeError(error_msg)

        # Validate dimension
        if len(vec) != TARGET_DIM:
            raise RuntimeError(f"Embedding dimension {len(vec)} != expected {TARGET_DIM}")

        embeddings.append(vec)
        time.sleep(0.1)  # Small delay between API calls to avoid rate limiting

    print(f"DEBUG: Successfully embedded {len(embeddings)} text chunks")
    return embeddings
