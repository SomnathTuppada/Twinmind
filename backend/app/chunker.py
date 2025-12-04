def chunk_text(text, chunk_size=800, overlap=150):
    words = text.split()
    chunks = []
    i = 0
    idx = 0
    while i < len(words):
        cwords = words[i:i+chunk_size]
        chunk = " ".join(cwords)
        chunks.append({"index": idx, "text": chunk})
        idx += 1
        i += chunk_size - overlap
    return chunks
