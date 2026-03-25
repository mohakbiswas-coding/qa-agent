# backend/main.py
import os
import sys
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Add the backend directory to Python path so imports work
sys.path.insert(0, os.path.dirname(__file__))

from knowledge_base import (
    build_knowledge_base,
    is_knowledge_base_ready,
    retrieve_relevant_chunks,
    get_html_content
)
from test_case_agent import generate_test_cases
from selenium_agent import generate_selenium_script

load_dotenv()

# ─── FastAPI App Setup ────────────────────────────────────────────────────────
app = FastAPI(
    title="QA Agent API",
    description="Autonomous QA Agent for Test Case and Script Generation",
    version="1.0.0"
)

# Allow Streamlit (running on port 8501) to call this API (on port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request/Response Models ──────────────────────────────────────────────────

class TestCaseRequest(BaseModel):
    prompt: str  # e.g., "Generate all test cases for the discount code feature"


class SeleniumScriptRequest(BaseModel):
    test_case: Dict[str, Any]   # The selected test case object
    html_content: Optional[str] = None  # Optional: HTML content


# ─── API Endpoints ────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "QA Agent API is running!", "status": "ok"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "knowledge_base_ready": is_knowledge_base_ready()
    }


@app.post("/build-knowledge-base")
async def build_kb(files: List[UploadFile] = File(...)):
    """
    Endpoint: Upload documents and build the vector knowledge base.
    
    Accepts multiple files (MD, TXT, JSON, HTML, PDF).
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    documents = []
    for file in files:
        content = await file.read()
        documents.append({
            "filename": file.filename,
            "content": content
        })
    
    result = build_knowledge_base(documents)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


@app.post("/generate-test-cases")
async def generate_tc(request: TestCaseRequest):
    """
    Endpoint: Generate test cases for a given feature prompt.
    """
    if not is_knowledge_base_ready():
        raise HTTPException(
            status_code=400,
            detail="Knowledge base not built yet. Please upload documents first."
        )
    
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    result = generate_test_cases(request.prompt)
    return result


@app.post("/generate-selenium-script")
async def generate_script(request: SeleniumScriptRequest):
    """
    Endpoint: Generate a Selenium Python script for a given test case.
    """
    if not is_knowledge_base_ready():
        raise HTTPException(
            status_code=400,
            detail="Knowledge base not built yet."
        )
    
    # If HTML not provided, try to get it from the knowledge base
    html_content = request.html_content or get_html_content()
    
    if not html_content:
        raise HTTPException(
            status_code=400,
            detail="No HTML content found. Please upload checkout.html as part of documents."
        )
    
    result = generate_selenium_script(request.test_case, html_content)
    return result


@app.get("/kb-status")
def kb_status():
    """Check if the knowledge base is ready."""
    return {"ready": is_knowledge_base_ready()}


# ─── Run Server ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
