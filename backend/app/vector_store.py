from pinecone import Pinecone
from app.config import settings
from app.embeddings import embed_batch

# Initialize Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Connect to your index
index = pc.Index(settings.PINECONE_INDEX)

def save_chunks_to_pinecone(source_id, user_id, chunks):
    print("DEBUG: Pinecone index in use =", settings.PINECONE_INDEX)

    texts = [c["text"] for c in chunks]
    vectors = embed_batch(texts)

    # DEBUG: show vector dimension of first vector
    if vectors and len(vectors) > 0:
        print("DEBUG: vector sent to Pinecone dim =", len(vectors[0]))
    else:
        print("DEBUG: no vectors generated")


    items = []
    for i, c in enumerate(chunks):
        metadata = {
            "source_id": source_id,
            "user_id": user_id,
            "chunk_index": c["index"],
            "page": c.get("page"),
            "text": c["text"]
        }
        item_id = f"{source_id}_{c['index']}"
        items.append({
            "id": item_id,
            "values": vectors[i],
            "metadata": metadata
        })

    # Upsert in batches
    index.upsert(items)
