# 🤖 QA Agent

A personal project that leverages AI to automate QA test case generation and Selenium script creation. The agent reads project documentation, builds a knowledge base, and intelligently generates test cases and automation scripts based on your project specifications.

## About

This project came from the idea of reducing manual test case creation. Instead of manually writing test cases from documentation, you can feed the agent your project specs and have it generate comprehensive test cases that cover happy paths, edge cases, and error scenarios. The generated test cases can then be automatically converted into runnable Selenium scripts.

The agent uses a Retrieval-Augmented Generation (RAG) approach—it parses your documentation, converts it into embeddings, stores it in a vector database, and retrieves relevant context when generating test cases. This ensures the generated tests are always aligned with your actual project requirements.

## How It Works

1. **Upload Documentation** → Agent parses PDFs, HTML, JSON, Markdown, text files
2. **Build Knowledge Base** → Documents are split into chunks and converted to embeddings, then stored in ChromaDB
3. **Generate Test Cases** → Feed a natural language prompt (e.g., "Test discount code validation"), and the agent retrieves relevant docs and generates structured test cases using LLaMA 3.3 70B
4. **Generate Selenium Scripts** → Pick a test case and convert it into a runnable Python script with Selenium

## Tech Stack

- **Backend:** FastAPI + Uvicorn (REST API for KB building and test generation)
- **Frontend:** Streamlit (interactive web interface)
- **LLM:** Groq API with LLaMA 3.3 70B (fast, free inference)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB:** ChromaDB (local persistent storage)
- **Document Parsing:** pdfplumber, BeautifulSoup4
- **Text Processing:** LangChain (text splitting and chunking)

## Project Structure

```
qa-agent/
├── backend/
│   ├── main.py                 # FastAPI server with KB and test generation endpoints
│   ├── knowledge_base.py       # Document parsing, chunking, embeddings, ChromaDB
│   ├── test_case_agent.py      # RAG-based test case generation
│   └── selenium_agent.py       # Selenium script generation
├── frontend/
│   └── app.py                  # Streamlit UI with 3-phase workflow
├── assets/                     # Example documentation files
│   ├── checkout.html
│   ├── product_specs.md
│   ├── validation_rules.md
│   ├── ui_ux_guide.txt
│   ├── api_endpoints.json
│   └── error_messages.md
└── chroma_db/                  # Local vector database storage
```

## Getting Started

Requires Python 3.13+, a free Groq API key (https://console.groq.com/keys), and the packages in `requirements.txt`.

Two servers run simultaneously:
- **Backend:** `http://localhost:8000` (FastAPI + Uvicorn)
- **Frontend:** `http://localhost:8501` (Streamlit)

## Features

- **Multi-format document support:** PDF, HTML, JSON, Markdown, plain text
- **Intelligent test case generation:** Uses LLM with RAG to generate contextually relevant test cases
- **Selenium automation:** Converts test cases into runnable Python scripts
- **Fast inference:** Groq's API provides quick LLM responses (free tier)
- **Persistent storage:** Knowledge bases are saved locally in ChromaDB
- **Interactive UI:** Clean Streamlit interface for easy document upload and testing

## Example Use Case

Included are example docs for an e-commerce checkout page:
- HTML page with product selection, cart, discount codes, shipping
- Product specs with discount rules (SAVE15 = 15% off)
- Form validation rules, UI/UX guidelines, API contracts, error messages

Upload these files and ask the agent to **"Generate test cases for the discount code feature"** or **"Create tests for form field validation"**—it will instantly produce structured test cases that reference the actual specs.

## Notes

- First run downloads the embedding model (~100MB), takes a few minutes
- ChromaDB stores data locally in `chroma_db/` folder
- All API interactions use the free tier of Groq's inference service
- Generated Selenium scripts require Chrome browser to run
