# backend/knowledge_base.py
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any

import pdfplumber
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb


# ─── Globals ──────────────────────────────────────────────────────────────────
# Load the embedding model once (it's large, loading it once is efficient)
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB stores data in a local folder called "chroma_db"
CHROMA_CLIENT = chromadb.PersistentClient(path="./chroma_db")
COLLECTION_NAME = "qa_knowledge_base"


# ─── Document Parsers ─────────────────────────────────────────────────────────

def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    import io
    pdf_file = io.BytesIO(file_bytes)
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
                text += "\n"
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text


def parse_html(content: str) -> str:
    """Extract meaningful text + structure from HTML."""
    soup = BeautifulSoup(content, "html.parser")
    
    # Get all text content
    text = soup.get_text(separator="\n", strip=True)
    
    # Also extract element IDs and names (useful for Selenium selectors)
    elements = []
    for tag in soup.find_all(True):
        if tag.get("id"):
            elements.append(f"Element ID: '{tag.get('id')}' (tag: {tag.name})")
        if tag.get("name"):
            elements.append(f"Element name: '{tag.get('name')}' (tag: {tag.name})")
    
    selector_info = "\n\nHTML ELEMENT SELECTORS FOUND:\n" + "\n".join(elements)
    return text + selector_info


def parse_json(content: str) -> str:
    """Convert JSON to readable text format."""
    try:
        data = json.loads(content)
        return json.dumps(data, indent=2)
    except json.JSONDecodeError:
        return content


def parse_document(filename: str, content: bytes) -> str:
    """Route to the right parser based on file extension."""
    ext = Path(filename).suffix.lower()
    
    if ext == ".pdf":
        return parse_pdf(content)
    elif ext in [".html", ".htm"]:
        return parse_html(content.decode("utf-8", errors="ignore"))
    elif ext == ".json":
        return parse_json(content.decode("utf-8", errors="ignore"))
    else:
        # For .txt, .md, and everything else, just decode as text
        return content.decode("utf-8", errors="ignore")


# ─── Knowledge Base Builder ───────────────────────────────────────────────────

def build_knowledge_base(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Main function: Takes a list of documents, parses them, chunks them,
    embeds them, and stores in ChromaDB.
    
    Args:
        documents: List of {"filename": str, "content": bytes}
    
    Returns:
        Summary dict with stats
    """
    # Delete old collection if it exists (fresh start)
    try:
        CHROMA_CLIENT.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    
    collection = CHROMA_CLIENT.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    
    # Text splitter: splits large text into overlapping chunks
    # chunk_size=500 means each chunk is ~500 characters
    # chunk_overlap=50 means chunks share 50 chars at edges (prevents losing context)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    all_chunks = []
    all_ids = []
    all_metadatas = []
    all_embeddings = []
    
    for doc in documents:
        filename = doc["filename"]
        content = doc["content"]
        
        # Parse document to text
        text = parse_document(filename, content)
        
        if not text.strip():
            continue
        
        # Split into chunks
        chunks = splitter.split_text(text)
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{i}"
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metadatas.append({
                "source_document": filename,
                "chunk_index": i
            })
    
    if not all_chunks:
        return {"status": "error", "message": "No text could be extracted from documents"}
    
    # Generate embeddings in batches (faster)
    print(f"Generating embeddings for {len(all_chunks)} chunks...")
    embeddings = EMBEDDING_MODEL.encode(all_chunks, show_progress_bar=True)
    all_embeddings = embeddings.tolist()
    
    # Store in ChromaDB
    collection.add(
        ids=all_ids,
        documents=all_chunks,
        embeddings=all_embeddings,
        metadatas=all_metadatas
    )
    
    return {
        "status": "success",
        "total_documents": len(documents),
        "total_chunks": len(all_chunks),
        "message": f"Knowledge base built with {len(all_chunks)} chunks from {len(documents)} documents."
    }


def retrieve_relevant_chunks(query: str, n_results: int = 5) -> List[Dict]:
    """
    Search the vector database for chunks relevant to the query.
    
    How it works:
    1. Embed the query (turn it into numbers)
    2. Find chunks whose numbers are most similar
    3. Return those chunks
    """
    try:
        collection = CHROMA_CLIENT.get_collection(COLLECTION_NAME)
    except Exception:
        return []
    
    # Embed the query
    query_embedding = EMBEDDING_MODEL.encode([query]).tolist()
    
    # Search
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"]
    )
    
    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        chunks.append({
            "text": doc,
            "source": results["metadatas"][0][i]["source_document"],
            "relevance_score": 1 - results["distances"][0][i]  # Convert distance to similarity
        })
    
    return chunks


def get_html_content() -> str:
    """Retrieve the stored HTML content from the knowledge base."""
    try:
        collection = CHROMA_CLIENT.get_collection(COLLECTION_NAME)
        results = collection.get(
            where={"source_document": {"$in": ["checkout.html"]}},
            include=["documents"]
        )
        if results["documents"]:
            return "\n".join(results["documents"])
        return ""
    except Exception:
        return ""


def is_knowledge_base_ready() -> bool:
    """Check if the knowledge base has been built."""
    try:
        collection = CHROMA_CLIENT.get_collection(COLLECTION_NAME)
        return collection.count() > 0
    except Exception:
        return False
