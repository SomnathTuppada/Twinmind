        # System Design (Text + Selectable PDF Prototype)

This document describes the ingestion, indexing, retrieval, and Q&A pipeline for the 'Second Brain' prototype supporting plain text and PDFs with selectable text.

## Components
- FastAPI backend
- PDF extractor (pdfplumber)
- Chunker (word-based with overlap)
- Embeddings (OpenAI by default)
- Vector DB (Chroma)
- LLM (Gemini Flash 2.5 via google.generativeai)

## Data flow
1. Upload PDF -> saved to /uploads
2. Background worker extracts per-page text -> chunk -> embed -> store in Chroma
3. Query endpoint retrieves top-k chunks -> assemble context -> call Gemini -> return answer + provenance

## Schema
- sources: id, title, user_id, created_at, raw_location
- chunks: chunk_id, source_id, page, chunk_index, text, char offsets, embedding_id

## Chunking
- chunk_size=800 words, overlap=150

## Temporal queries
- Chroma metadata contains created_at and can be filtered using 'where' parameter

## Privacy
- Namespace entries by user_id
- Allow deletion of source -> remove chunks


