# 🤖 Autonomous QA Agent

An intelligent QA agent that builds a "testing brain" from project documentation and generates comprehensive test cases and Selenium automation scripts.

## 🛠️ Tech Stack
- **Backend:** FastAPI + Uvicorn
- **Frontend:** Streamlit
- **AI/LLM:** Groq API (LLaMA 3.3 70B - llama-3.3-70b-versatile) — free tier
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB:** ChromaDB
- **Document Parsing:** PyMuPDF, BeautifulSoup4

## 📋 Prerequisites
- Python 3.10+
- Chrome browser (for running Selenium scripts)
- Groq API key (free at https://console.groq.com)

## ⚡ Quick Start

### 1. Clone and setup
```bash
git clone https://github.com/YOUR_USERNAME/qa-agent.git
cd qa-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API key
Create `.env` in root:
```
GROQ_API_KEY=your_key_here
```

### 3. Start the backend (Terminal 1)
```bash
cd backend
python main.py
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 4. Start the frontend (Terminal 2)
```bash
cd frontend
streamlit run app.py
# UI opens at http://localhost:8501
```

## 📁 Support Documents Included
| File | Purpose |
|------|---------|
| `checkout.html` | Target e-commerce checkout page |
| `product_specs.md` | Discount codes, pricing, shipping rules |
| `ui_ux_guide.txt` | UI validation rules, button colors, error styling |
| `api_endpoints.json` | API contract for coupon and order endpoints |
| `validation_rules.md` | Detailed form validation rules |
| `error_messages.md` | All error messages and their element IDs |

## 🚀 Usage
1. Open http://localhost:8501
2. Upload all files from `assets/` folder
3. Click "Build Knowledge Base"
4. Type a prompt: *"Generate test cases for the discount code feature"*
5. Click "Generate Test Cases"
6. Select a test case → Click "Generate Selenium Script"
7. Download and run the script!

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: groq` | Package not installed | `pip install groq` |
| `ConnectionError: localhost:8000` | Backend not started | Run `python main.py` in backend/ |
| `GROQ_API_KEY not found` | .env missing or wrong path | Check `.env` file is in project root |
| `Collection not found` | KB not built | Click "Build Knowledge Base" first |
| Slow embedding generation | First run downloads model | Wait 2-3 min, model downloads once |
| ChromaDB error on Windows | Path issue | Run from project root, not backend/ |

## 📚 Useful Documentation Links

- FastAPI docs: https://fastapi.tiangolo.com
- Streamlit docs: https://docs.streamlit.io
- ChromaDB docs: https://docs.trychroma.com
- Groq API docs: https://console.groq.com/docs
- sentence-transformers: https://www.sbert.net
- Selenium Python docs: https://selenium-python.readthedocs.io
- LangChain text splitters: https://python.langchain.com/docs/modules/data_connection/document_transformers/
