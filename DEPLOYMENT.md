# QA Agent Deployment Guide

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Cloud (UI)                      │
│                  http://username.streamlit.app              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ (API calls)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Render (Backend API)                            │
│         https://qa-agent-backend.onrender.com               │
│              (FastAPI + Uvicorn)                             │
└──────────────────────────────────────────────────────────────┘
                       │
                       │ (Groq API Calls)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 Groq Cloud (LLM)                             │
│            api.groq.com (llama-3.3-70b-versatile)           │
└──────────────────────────────────────────────────────────────┘
```

## Step-by-Step Deployment on Render

### Phase 1: Prepare Your Repository

1. **Initialize Git (if not already)**
   ```bash
   cd c:\Users\Mohak\Projects\qa-agent
   git init
   git config user.name "Your Name"
   git config user.email "your@email.com"
   ```

2. **Commit all files**
   ```bash
   git add .
   git commit -m "Initial QA Agent commit"
   git branch -M main
   ```

3. **Create GitHub Repository**
   - Go to https://github.com/new
   - Create repo named `qa-agent`
   - Copy the remote URL

4. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/qa-agent.git
   git push -u origin main
   ```

### Phase 2: Deploy Backend on Render

1. **Sign up on Render**
   - Go to https://render.com
   - Sign up with GitHub (fastest)

2. **Create New Web Service**
   - Dashboard → "New+" → "Web Service"
   - Connect your GitHub account
   - Select `qa-agent` repository
   - Proceed

3. **Configure Service**
   - **Name:** `qa-agent-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd backend && python main.py`
   - **Plan:** Free (or Paid if you want better uptime)

4. **Add Environment Variables**
   - Click "Environment"
   - Add these variables:
     ```
     GROQ_API_KEY = your_groq_api_key_here
     ENV = production
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically (takes ~2-3 minutes)
   - Your backend URL will be: `https://qa-agent-backend.onrender.com`

### Phase 3: Deploy Frontend on Streamlit Cloud

1. **Sign up on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign up with GitHub

2. **Deploy Application**
   - Click "New app"
   - Select:
     - Repository: `YOUR_USERNAME/qa-agent`
     - Branch: `main`
     - Main file path: `frontend/app.py`
   - Click "Deploy"

3. **Configure Secrets**
   - Go to App Settings (gear icon)
   - Click "Secrets"
   - Add these secrets:
     ```
     API_BASE_URL = https://qa-agent-backend.onrender.com
     GROQ_API_KEY = your_groq_api_key_here
     ```

4. **Customize App**
   - App settings → General → Rename app (optional)
   - Your app URL: `https://YOUR_STREAMLIT_USERNAME-qa-agent.streamlit.app`

### Phase 4: Update Frontend Code

Your frontend needs to read the backend URL from environment:

Edit `frontend/app.py` and ensure it has:

```python
import streamlit as st
import os

# Get API URL from secrets or environment
API_BASE_URL = st.secrets.get("API_BASE_URL") or os.getenv("API_BASE_URL", "http://localhost:8000")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY", "")
```

Then use `API_BASE_URL` in all API calls instead of hardcoded localhost.

---

## Troubleshooting

### Backend won't start on Render

**Problem:** "Failed to start application"

**Solution:**
- Check Build Logs: Dashboard → Service → Logs
- Ensure `Procfile` exists in root directory
- Verify `requirements.txt` has all dependencies

```bash
# Update requirements.txt locally first
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### API connection fails from Streamlit

**Problem:** "Failed to connect to backend"

**Solution:**
1. Verify backend is running: Visit `https://qa-agent-backend.onrender.com/health`
2. Check Streamlit Secrets has correct `API_BASE_URL`
3. Backend needs CORS enabled (already configured in code)

### ChromaDB errors on Render

**Problem:** "Permission denied" or "File not found" for chroma_db

**Solution:**
Render's filesystem is ephemeral (data is lost on restarts). To fix:

Option A: Store in memory (simpler, but loses data)
Edit `backend/knowledge_base.py`:
```python
# Change this line:
CHROMA_CLIENT = chromadb.PersistentClient(path="./chroma_db")

# To this:
CHROMA_CLIENT = chromadb.EphemeralClient()
```

Option B: Use Render Postgres addon (advanced)
- Add Postgres service on Render
- Update ChromaDB to use Postgres

### Slow cold starts

**Problem:** First request takes 30+ seconds

**Solution:**
- Free tier on Render spins down after 15 minutes of inactivity
- Upgrade to Paid plan for better performance
- Or use a "Pinger" service to keep it warm

### GROQ_API_KEY not working

**Problem:** "Invalid API key"

**Solution:**
1. Get fresh key from https://console.groq.com/keys
2. Verify it's in Render environment variables (not in code)
3. Verify it's in Streamlit Cloud secrets
4. Restart the service for changes to take effect

---

## Monitoring & Logs

### Render Backend Logs
- Dashboard → qa-agent-backend → Logs
- Shows all API requests and errors
- Filter by status code or timestamp

### Streamlit Logs
- Dashboard → qa-agent (frontend) → Logs
- Shows UI errors and debug info

### Health Check
Check if backend is alive:
```bash
curl https://qa-agent-backend.onrender.com/health -v
```

Should return:
```json
{
  "status": "ok",
  "services": {
    "groq": "ok",
    "chroma": "ok"
  }
}
```

---

## Cost Analysis

| Service | Tier | Cost | Notes |
|---------|------|------|-------|
| Render Backend | Free | $0 | 15 min auto-sleep, 0.5 GB RAM |
| Render Backend | Starter | $7/mo | Always running, recommended |
| Streamlit Cloud | Community | $0 | 1 GB RAM, perfect for UI |
| Groq API | Free | $0 | Rate limited, sufficient for personal use |
| **Total** | | **$0-7/mo** | Fully functional deployment |

---

## File Structure After Deployment Setup

```
qa-agent/
├── Procfile                    # Render entry point
├── render.yaml                 # Infrastructure as code (optional)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .streamlit/
│   └── config.toml            # Streamlit theming
├── backend/
│   ├── main.py                # FastAPI server
│   ├── knowledge_base.py       # KB management
│   ├── test_case_agent.py      # Test generation
│   └── selenium_agent.py       # Script generation
├── frontend/
│   └── app.py                 # Streamlit UI
└── assets/
    ├── checkout.html
    ├── product_specs.md
    ├── validation_rules.md
    ├── ui_ux_guide.txt
    ├── api_endpoints.json
    └── error_messages.md
```

---

## Next Steps

1. ✅ Commit and push code to GitHub
2. ✅ Deploy backend on Render
3. ✅ Deploy frontend on Streamlit Cloud
4. ✅ Test the deployed application
5. ✅ Share your app URL with others
6. 📈 Monitor logs and performance
7. 💰 Upgrade to paid tier if needed (optional)

---

## Quick Redeploy

To update your deployed apps:

```bash
# Make code changes
nano backend/main.py  # or edit in VS Code

# Commit and push
git add .
git commit -m "Update backend logic"
git push

# Both Render and Streamlit Cloud auto-redeploy on git push!
```

No manual redeployment needed—CI/CD is automatic.
