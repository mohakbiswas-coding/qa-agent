# 🤖 Complete Guide: Autonomous QA Agent Project
### Beginner-Friendly Step-by-Step Tutorial

---

## 📖 What We're Building

A web app where you can:
1. Upload your project documents (specs, guides, etc.) + an HTML file
2. The app builds a "knowledge brain" from them (vector database)
3. Ask it to generate test cases grounded in those documents
4. Pick a test case and auto-generate a runnable Selenium Python script

**Tech Stack:**
| What | Tool | Why |
|------|------|-----|
| Backend API | FastAPI (Python) | Easy, fast, modern |
| Frontend UI | Streamlit (Python) | No HTML/CSS needed, just Python |
| AI / LLM | Groq API (free) | Free tier, super fast |
| Embeddings | sentence-transformers | Free, runs locally |
| Vector DB | ChromaDB | Easy, no server needed |
| Document parsing | PyMuPDF, BeautifulSoup | Handles PDF, HTML, TXT, JSON |

---

## 🗂️ Final Project Structure

```
qa-agent/
├── backend/
│   ├── main.py              ← FastAPI server (all API routes)
│   ├── knowledge_base.py    ← Document parsing + vector DB logic
│   ├── test_case_agent.py   ← AI agent to generate test cases
│   └── selenium_agent.py    ← AI agent to generate Selenium scripts
├── frontend/
│   └── app.py               ← Streamlit UI
├── assets/
│   ├── checkout.html        ← The target web page to test
│   ├── product_specs.md     ← Support doc 1
│   ├── ui_ux_guide.txt      ← Support doc 2
│   ├── api_endpoints.json   ← Support doc 3
│   ├── validation_rules.md  ← Support doc 4
│   └── error_messages.md    ← Support doc 5
├── chroma_db/               ← Auto-created: vector database storage
├── .env                     ← Your secret API keys (never commit this!)
├── requirements.txt         ← Python dependencies
└── README.md                ← Project documentation
```

---

## STEP 1: Install Prerequisites

### 1.1 Install Python 3.10+

Check your version first:
```bash
python --version
# or
python3 --version
```

If you don't have Python 3.10+, download from: https://www.python.org/downloads/

### 1.2 Install Git

Download from: https://git-scm.com/downloads

Verify:
```bash
git --version
```

### 1.3 Install VS Code (Recommended Editor)

Download from: https://code.visualstudio.com/

Install these VS Code extensions:
- Python (by Microsoft)
- Pylance

---

## STEP 2: Set Up GitHub Repository

### 2.1 Create a GitHub Account
Go to https://github.com and sign up if you don't have an account.

### 2.2 Create a New Repository
1. Click the **"+"** button (top right) → "New repository"
2. Name it: `qa-agent`
3. Select **Public** (or Private)
4. Check **"Add a README file"**
5. Click **"Create repository"**

### 2.3 Clone the Repository to Your Computer
```bash
# Open your terminal / command prompt
# Navigate to where you want the project folder
cd Desktop   # or wherever you like

# Clone (replace YOUR_USERNAME with your GitHub username)
git clone https://github.com/YOUR_USERNAME/qa-agent.git

# Go into the folder
cd qa-agent
```

### 2.4 Open in VS Code
```bash
code .
```

---

## STEP 3: Get Your Free Groq API Key

Groq gives you a **free API** to use powerful AI models (like LLaMA 3).

1. Go to https://console.groq.com
2. Sign up for free
3. Click **"API Keys"** → **"Create API Key"**
4. Copy the key (it starts with `gsk_...`)

> ⚠️ Keep this key SECRET. Never paste it in your code directly.

---

## STEP 4: Set Up the Project

### 4.1 Create the Folder Structure
Open the terminal in VS Code (`View → Terminal`) and run:

```bash
# Create all folders
mkdir backend frontend assets chroma_db

# Create all files (on Windows use: type nul > filename)
# On Mac/Linux:
touch backend/main.py
touch backend/knowledge_base.py
touch backend/test_case_agent.py
touch backend/selenium_agent.py
touch frontend/app.py
touch .env
touch requirements.txt
touch README.md
```

### 4.2 Create the `.env` File
Open `.env` and add:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```
Replace `your_actual_groq_api_key_here` with the key you got from Groq.

### 4.3 Create `.gitignore`
Create a file called `.gitignore` and paste:
```
.env
chroma_db/
__pycache__/
*.pyc
.DS_Store
venv/
*.egg-info/
```
This prevents your secret key and generated files from going to GitHub.

### 4.4 Create Virtual Environment & Install Dependencies

```bash
# Create a virtual environment (isolates your project's packages)
python -m venv venv

# Activate it:
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# You should now see (venv) at the start of your terminal line
```

### 4.5 Create `requirements.txt`
Paste this into `requirements.txt`:
```
fastapi==0.111.0
uvicorn==0.30.1
streamlit==1.35.0
python-dotenv==1.0.1
groq==0.9.0
chromadb==0.5.3
sentence-transformers==3.0.1
langchain==0.2.6
langchain-community==0.2.6
langchain-text-splitters==0.2.2
pymupdf==1.24.5
beautifulsoup4==4.12.3
python-multipart==0.0.9
requests==2.32.3
pydantic==2.7.4
httpx==0.27.0
```

### 4.6 Install Everything
```bash
pip install -r requirements.txt
```
⏳ This will take 3-10 minutes. The `sentence-transformers` package is large.

---

## STEP 5: Create the Support Documents (Project Assets)

These are the documents your AI will learn from.

### 5.1 Create `assets/checkout.html`
This is the e-commerce checkout page your tests will run against.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>E-Shop Checkout</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
    .product-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
    .cart-section { background: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0; }
    .cart-item { display: flex; justify-content: space-between; align-items: center; margin: 10px 0; }
    .form-group { margin: 15px 0; }
    label { display: block; margin-bottom: 5px; font-weight: bold; }
    input[type="text"], input[type="email"] { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    .error { color: red; font-size: 0.85em; display: none; }
    .error.visible { display: block; }
    .radio-group { margin: 10px 0; }
    .radio-group label { font-weight: normal; display: inline; margin-left: 5px; }
    #pay-now-btn { background-color: green; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%; }
    #pay-now-btn:hover { background-color: darkgreen; }
    #success-message { color: green; font-size: 1.2em; text-align: center; display: none; padding: 20px; }
    .discount-section { display: flex; gap: 10px; margin: 15px 0; }
    #total-price { font-size: 1.3em; font-weight: bold; }
    #discount-msg { color: green; font-size: 0.9em; }
    #discount-error { color: red; font-size: 0.9em; }
    .add-to-cart-btn { background: #007bff; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; }
    .qty-input { width: 50px; text-align: center; padding: 5px; border: 1px solid #ccc; border-radius: 3px; }
  </style>
</head>
<body>
  <h1>E-Shop Checkout</h1>

  <!-- Products Section -->
  <h2>Products</h2>
  <div class="product-card">
    <div>
      <strong>Wireless Headphones</strong>
      <p>$49.99</p>
    </div>
    <button class="add-to-cart-btn" id="add-headphones" onclick="addToCart('Wireless Headphones', 49.99)">Add to Cart</button>
  </div>
  <div class="product-card">
    <div>
      <strong>Laptop Stand</strong>
      <p>$29.99</p>
    </div>
    <button class="add-to-cart-btn" id="add-laptop-stand" onclick="addToCart('Laptop Stand', 29.99)">Add to Cart</button>
  </div>
  <div class="product-card">
    <div>
      <strong>USB-C Hub</strong>
      <p>$39.99</p>
    </div>
    <button class="add-to-cart-btn" id="add-usb-hub" onclick="addToCart('USB-C Hub', 39.99)">Add to Cart</button>
  </div>

  <!-- Cart Summary -->
  <div class="cart-section">
    <h2>Cart Summary</h2>
    <div id="cart-items"></div>
    <hr>
    <div class="discount-section">
      <input type="text" id="discount-code" placeholder="Enter discount code" />
      <button id="apply-discount-btn" onclick="applyDiscount()">Apply</button>
    </div>
    <p id="discount-msg"></p>
    <p id="discount-error"></p>
    <p>Total: <span id="total-price">$0.00</span></p>
  </div>

  <!-- User Details Form -->
  <h2>Your Details</h2>
  <form id="checkout-form">
    <div class="form-group">
      <label for="name">Full Name *</label>
      <input type="text" id="name" name="name" placeholder="John Doe" />
      <span class="error" id="name-error">Name is required.</span>
    </div>
    <div class="form-group">
      <label for="email">Email Address *</label>
      <input type="text" id="email" name="email" placeholder="john@example.com" />
      <span class="error" id="email-error">Please enter a valid email address.</span>
    </div>
    <div class="form-group">
      <label for="address">Shipping Address *</label>
      <input type="text" id="address" name="address" placeholder="123 Main St, City, Country" />
      <span class="error" id="address-error">Address is required.</span>
    </div>

    <!-- Shipping Method -->
    <h3>Shipping Method</h3>
    <div class="radio-group">
      <input type="radio" name="shipping" id="standard-shipping" value="standard" checked />
      <label for="standard-shipping">Standard Shipping (Free)</label>
    </div>
    <div class="radio-group">
      <input type="radio" name="shipping" id="express-shipping" value="express" />
      <label for="express-shipping">Express Shipping ($10.00)</label>
    </div>

    <!-- Payment Method -->
    <h3>Payment Method</h3>
    <div class="radio-group">
      <input type="radio" name="payment" id="credit-card" value="credit_card" checked />
      <label for="credit-card">Credit Card</label>
    </div>
    <div class="radio-group">
      <input type="radio" name="payment" id="paypal" value="paypal" />
      <label for="paypal">PayPal</label>
    </div>

    <br>
    <button type="button" id="pay-now-btn" onclick="submitPayment()">Pay Now</button>
  </form>

  <div id="success-message">✅ Payment Successful! Thank you for your order.</div>

  <script>
    let cart = [];
    let baseTotal = 0;
    let discountApplied = false;
    let discountPercent = 0;

    function addToCart(name, price) {
      const existing = cart.find(i => i.name === name);
      if (existing) {
        existing.qty += 1;
      } else {
        cart.push({ name, price, qty: 1 });
      }
      renderCart();
    }

    function renderCart() {
      const container = document.getElementById('cart-items');
      container.innerHTML = '';
      baseTotal = 0;
      cart.forEach((item, index) => {
        baseTotal += item.price * item.qty;
        container.innerHTML += `
          <div class="cart-item">
            <span>${item.name}</span>
            <input type="number" class="qty-input" id="qty-${index}" value="${item.qty}" min="1"
              onchange="updateQty(${index}, this.value)" />
            <span>$${(item.price * item.qty).toFixed(2)}</span>
          </div>`;
      });
      updateTotal();
    }

    function updateQty(index, val) {
      cart[index].qty = parseInt(val) || 1;
      renderCart();
    }

    function updateTotal() {
      let total = baseTotal;
      const shippingVal = document.querySelector('input[name="shipping"]:checked').value;
      if (shippingVal === 'express') total += 10;
      if (discountApplied) total = total * (1 - discountPercent / 100);
      document.getElementById('total-price').textContent = '$' + total.toFixed(2);
    }

    function applyDiscount() {
      const code = document.getElementById('discount-code').value.trim().toUpperCase();
      const msgEl = document.getElementById('discount-msg');
      const errEl = document.getElementById('discount-error');
      if (code === 'SAVE15') {
        discountApplied = true;
        discountPercent = 15;
        msgEl.textContent = '✅ Discount applied: 15% off!';
        errEl.textContent = '';
        updateTotal();
      } else {
        discountApplied = false;
        discountPercent = 0;
        errEl.textContent = '❌ Invalid discount code.';
        msgEl.textContent = '';
        updateTotal();
      }
    }

    function validateForm() {
      let valid = true;
      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const address = document.getElementById('address').value.trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      document.getElementById('name-error').classList.remove('visible');
      document.getElementById('email-error').classList.remove('visible');
      document.getElementById('address-error').classList.remove('visible');

      if (!name) { document.getElementById('name-error').classList.add('visible'); valid = false; }
      if (!email || !emailRegex.test(email)) { document.getElementById('email-error').classList.add('visible'); valid = false; }
      if (!address) { document.getElementById('address-error').classList.add('visible'); valid = false; }
      return valid;
    }

    function submitPayment() {
      if (validateForm()) {
        document.getElementById('checkout-form').style.display = 'none';
        document.getElementById('success-message').style.display = 'block';
      }
    }

    // Update total when shipping changes
    document.querySelectorAll('input[name="shipping"]').forEach(r => r.addEventListener('change', updateTotal));
  </script>
</body>
</html>
```

### 5.2 Create `assets/product_specs.md`
```markdown
# Product Specifications - E-Shop Checkout

## Discount Codes
- The discount code `SAVE15` applies a 15% discount to the cart total.
- Discount codes are case-insensitive (SAVE15 = save15).
- Only one discount code can be applied per order.
- If an invalid code is entered, the system must show an error message.
- Discount is applied BEFORE shipping costs are added.

## Shipping Options
- Standard Shipping: Free of charge. Estimated 5-7 business days.
- Express Shipping: Costs $10.00. Estimated 1-2 business days.
- Shipping method must be selected before payment.

## Products Available
1. Wireless Headphones - $49.99
2. Laptop Stand - $29.99
3. USB-C Hub - $39.99

## Cart Behavior
- Users can add multiple quantities of the same item.
- Quantity can be updated from the cart summary section.
- Total price updates dynamically as quantity or shipping changes.

## Payment
- Supported methods: Credit Card, PayPal
- Clicking "Pay Now" validates the form first.
- On success, display "Payment Successful!" message.
- The form disappears after successful payment.
```

### 5.3 Create `assets/ui_ux_guide.txt`
```
UI/UX Guidelines - E-Shop Checkout

FORM VALIDATION:
- All required fields must show an inline error message when left empty.
- Error messages must be displayed in RED text directly below the input field.
- Error messages should disappear when the user corrects the field.
- Required fields: Name, Email, Address.

BUTTON STYLES:
- The "Pay Now" button MUST be green (#008000 or similar green shade).
- "Add to Cart" buttons should be blue.
- "Apply" (discount) button should be visible and next to the discount input.

SUCCESS FEEDBACK:
- After successful payment, show a green success message: "Payment Successful!"
- The checkout form must be hidden after successful payment.
- Success message must be clearly visible (large text, green color).

DISCOUNT SECTION:
- A text input and an "Apply" button must be side by side.
- Valid code feedback must appear in green.
- Invalid code feedback must appear in red.

CART:
- Each cart item must show: product name, quantity input, and price.
- Total price must update dynamically without page reload.

ACCESSIBILITY:
- All form fields must have associated labels.
- Buttons must have descriptive text.
```

### 5.4 Create `assets/api_endpoints.json`
```json
{
  "base_url": "http://localhost:8000",
  "endpoints": {
    "POST /apply_coupon": {
      "description": "Validate and apply a discount coupon code",
      "request_body": {
        "code": "string"
      },
      "responses": {
        "200": {
          "valid": true,
          "discount_percent": 15,
          "message": "Discount applied: 15% off"
        },
        "400": {
          "valid": false,
          "message": "Invalid discount code"
        }
      }
    },
    "POST /submit_order": {
      "description": "Submit the checkout order",
      "request_body": {
        "name": "string",
        "email": "string",
        "address": "string",
        "shipping_method": "standard | express",
        "payment_method": "credit_card | paypal",
        "cart_items": "array",
        "discount_code": "string (optional)"
      },
      "responses": {
        "200": {
          "status": "success",
          "order_id": "string",
          "message": "Payment Successful!"
        },
        "422": {
          "status": "error",
          "errors": ["Name is required", "Invalid email format"]
        }
      }
    },
    "GET /products": {
      "description": "Get list of available products",
      "responses": {
        "200": [
          {"id": 1, "name": "Wireless Headphones", "price": 49.99},
          {"id": 2, "name": "Laptop Stand", "price": 29.99},
          {"id": 3, "name": "USB-C Hub", "price": 39.99}
        ]
      }
    }
  }
}
```

### 5.5 Create `assets/validation_rules.md`
```markdown
# Form Validation Rules

## Name Field (id="name")
- REQUIRED: Cannot be empty or whitespace only.
- Error message: "Name is required."
- Error element id: "name-error"
- Must show error in red text when empty on form submission.

## Email Field (id="email")
- REQUIRED: Cannot be empty.
- FORMAT: Must match standard email format (user@domain.com).
- Error message: "Please enter a valid email address."
- Error element id: "email-error"
- Must reject: "notanemail", "missing@", "@nodomain"
- Must accept: "user@example.com", "test.name+tag@domain.co"

## Address Field (id="address")
- REQUIRED: Cannot be empty or whitespace only.
- Error message: "Address is required."
- Error element id: "address-error"

## Validation Trigger
- Validation runs when "Pay Now" button is clicked.
- All errors shown simultaneously (not one at a time).
- Errors must be hidden when the user fixes the field and resubmits.

## Cart Validation
- Cart does not need to have items for the form to be submitted.
- Quantity input must accept only positive integers (min=1).
```

### 5.6 Create `assets/error_messages.md`
```markdown
# Error Messages Reference

## Form Errors (shown inline in red)
| Field   | Element ID    | Error Message                              |
|---------|---------------|--------------------------------------------|
| Name    | name-error    | "Name is required."                        |
| Email   | email-error   | "Please enter a valid email address."      |
| Address | address-error | "Address is required."                     |

## Discount Code Errors
| Condition     | Element ID       | Message                    | Color |
|---------------|------------------|----------------------------|-------|
| Invalid code  | discount-error   | "❌ Invalid discount code." | red   |
| Valid code    | discount-msg     | "✅ Discount applied: 15% off!" | green |

## Payment Success
| Condition       | Element ID        | Message                                        |
|-----------------|-------------------|------------------------------------------------|
| Payment success | success-message   | "✅ Payment Successful! Thank you for your order." |

## General Rules
- Never show success and error messages simultaneously for the same field.
- Error elements use CSS class "error" and become visible with class "visible".
- The success-message div is hidden by default (display: none) and shown after valid payment.
```

---

## STEP 6: Write the Backend Code

### 6.1 `backend/knowledge_base.py`

This file handles:
- Parsing different document types (PDF, TXT, MD, JSON, HTML)
- Splitting text into chunks
- Creating embeddings (numerical representations of text)
- Storing in ChromaDB

```python
# backend/knowledge_base.py
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any

import fitz  # PyMuPDF
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
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
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
```

### 6.2 `backend/test_case_agent.py`

This file:
- Takes a user's prompt (e.g., "Generate test cases for the discount code feature")
- Retrieves relevant document chunks from ChromaDB
- Sends everything to the LLM (Groq/LLaMA)
- Returns structured test cases

```python
# backend/test_case_agent.py
import os
import json
import re
from typing import List, Dict, Any

from groq import Groq
from dotenv import load_dotenv
from knowledge_base import retrieve_relevant_chunks

load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama3-70b-8192"  # Best free model on Groq


def generate_test_cases(user_prompt: str) -> Dict[str, Any]:
    """
    Generate test cases using RAG (Retrieval-Augmented Generation).
    
    Steps:
    1. Retrieve relevant documentation chunks
    2. Build a detailed prompt for the LLM
    3. Call the LLM (Groq)
    4. Parse and return structured test cases
    """
    
    # Step 1: Retrieve relevant context from our knowledge base
    relevant_chunks = retrieve_relevant_chunks(user_prompt, n_results=8)
    
    if not relevant_chunks:
        return {
            "status": "error",
            "message": "Knowledge base is empty. Please build it first."
        }
    
    # Step 2: Format context for the prompt
    context_text = ""
    for i, chunk in enumerate(relevant_chunks, 1):
        context_text += f"\n--- Context {i} (from: {chunk['source']}) ---\n"
        context_text += chunk["text"] + "\n"
    
    # Step 3: Build the system + user prompt
    system_prompt = """You are an expert QA Engineer specializing in web application testing.
Your job is to generate comprehensive test cases based STRICTLY on the provided documentation.

IMPORTANT RULES:
1. Only generate test cases for features that are EXPLICITLY mentioned in the provided context.
2. Do NOT invent features that are not in the documentation.
3. Every test case MUST reference the source document it came from.
4. Generate both POSITIVE (happy path) and NEGATIVE (error/edge case) test cases.
5. Output MUST be valid JSON only - no extra text, no markdown code blocks, just JSON.

Output format - a JSON array of test case objects:
[
  {
    "test_id": "TC-001",
    "feature": "Feature name",
    "test_type": "Positive" or "Negative",
    "test_scenario": "Description of what is being tested",
    "preconditions": "What needs to be true before this test",
    "test_steps": ["Step 1", "Step 2", "Step 3"],
    "expected_result": "What should happen",
    "grounded_in": "source_document.md"
  }
]"""

    user_message = f"""Based on the following documentation, {user_prompt}

=== DOCUMENTATION CONTEXT ===
{context_text}
=== END CONTEXT ===

Generate comprehensive test cases. Remember: ONLY use features mentioned in the context above.
Return ONLY a valid JSON array, no other text."""

    # Step 4: Call Groq API
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.1,   # Low temperature = more consistent, less random
        max_tokens=4096
    )
    
    raw_output = response.choices[0].message.content.strip()
    
    # Step 5: Parse the JSON response
    # Sometimes LLMs wrap JSON in markdown code blocks - strip those
    raw_output = re.sub(r"```json\s*", "", raw_output)
    raw_output = re.sub(r"```\s*", "", raw_output)
    
    try:
        test_cases = json.loads(raw_output)
        return {
            "status": "success",
            "test_cases": test_cases,
            "context_used": [c["source"] for c in relevant_chunks],
            "count": len(test_cases)
        }
    except json.JSONDecodeError as e:
        # If JSON parsing fails, return the raw output with an error
        return {
            "status": "partial",
            "raw_output": raw_output,
            "error": f"Could not parse JSON: {str(e)}",
            "test_cases": []
        }
```

### 6.3 `backend/selenium_agent.py`

This file generates runnable Selenium Python scripts from a test case.

```python
# backend/selenium_agent.py
import os
import re
from typing import Dict, Any

from groq import Groq
from dotenv import load_dotenv
from knowledge_base import retrieve_relevant_chunks

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama3-70b-8192"


def generate_selenium_script(test_case: Dict, html_content: str) -> Dict[str, Any]:
    """
    Generate a runnable Selenium Python script for a given test case.
    
    Args:
        test_case: The test case dict (from test_case_agent)
        html_content: The full HTML of checkout.html
    
    Returns:
        Dict with the generated script
    """
    
    # Get relevant documentation for extra context
    query = f"{test_case.get('feature', '')} {test_case.get('test_scenario', '')}"
    relevant_chunks = retrieve_relevant_chunks(query, n_results=4)
    
    context_text = ""
    for chunk in relevant_chunks:
        context_text += f"\n[From {chunk['source']}]: {chunk['text']}\n"
    
    # Format test case nicely for the prompt
    test_case_text = f"""
Test ID: {test_case.get('test_id', 'TC-001')}
Feature: {test_case.get('feature', '')}
Test Type: {test_case.get('test_type', 'Positive')}
Scenario: {test_case.get('test_scenario', '')}
Preconditions: {test_case.get('preconditions', 'None')}
Steps: {'; '.join(test_case.get('test_steps', []))}
Expected Result: {test_case.get('expected_result', '')}
Grounded In: {test_case.get('grounded_in', '')}
"""
    
    system_prompt = """You are an expert Selenium WebDriver automation engineer using Python.

Generate a complete, runnable Selenium Python test script with these requirements:
1. Use selenium 4.x with Chrome WebDriver
2. Use webdriver_manager for automatic ChromeDriver management
3. Use EXACT element IDs, names, and CSS selectors from the provided HTML
4. Include proper waits (WebDriverWait / expected_conditions)
5. Include clear comments explaining each step
6. Include proper setup (driver initialization) and teardown (driver.quit())
7. Use unittest or direct script format (prefer direct script for simplicity)
8. Handle assertions properly - use assert statements with clear messages
9. The script must be 100% executable with: pip install selenium webdriver-manager

Output ONLY the Python code, no markdown, no explanation text outside the code."""

    user_message = f"""Generate a Selenium Python script for this test case:

{test_case_text}

=== HTML STRUCTURE OF THE PAGE ===
{html_content[:8000]}  
=== END HTML ===

=== RELEVANT DOCUMENTATION ===
{context_text}
=== END DOCS ===

Important: Use the EXACT element IDs from the HTML (e.g., id="name", id="email", id="pay-now-btn", etc.)
The HTML file is served locally, so use: driver.get("file:///path/to/checkout.html") 
or driver.get("http://localhost:8080/checkout.html")

Generate only the Python code."""

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.1,
        max_tokens=4096
    )
    
    script = response.choices[0].message.content.strip()
    
    # Clean up markdown if present
    script = re.sub(r"```python\s*", "", script)
    script = re.sub(r"```\s*", "", script)
    
    return {
        "status": "success",
        "script": script,
        "test_id": test_case.get("test_id", "TC-001"),
        "test_scenario": test_case.get("test_scenario", "")
    }
```

### 6.4 `backend/main.py`

This is the FastAPI server — it exposes HTTP endpoints that the Streamlit frontend calls.

```python
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
```

---

## STEP 7: Write the Frontend (Streamlit)

### `frontend/app.py`

```python
# frontend/app.py
import json
import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://localhost:8000"

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 QA Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stButton > button { width: 100%; }
    .success-box { background-color: #d4edda; border: 1px solid #c3e6cb;
                   padding: 15px; border-radius: 5px; color: #155724; }
    .error-box   { background-color: #f8d7da; border: 1px solid #f5c6cb;
                   padding: 15px; border-radius: 5px; color: #721c24; }
    .info-box    { background-color: #d1ecf1; border: 1px solid #bee5eb;
                   padding: 15px; border-radius: 5px; color: #0c5460; }
    .test-case-card { border: 1px solid #ddd; padding: 15px; border-radius: 8px;
                      margin: 10px 0; background: #f9f9f9; }
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("🤖 Autonomous QA Agent")
st.markdown("*Upload your project documents → Build Knowledge Base → Generate Test Cases → Generate Selenium Scripts*")
st.divider()


# ─── Helper Functions ─────────────────────────────────────────────────────────

def check_api_health():
    """Check if the backend API is running."""
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.status_code == 200, r.json()
    except Exception:
        return False, {}


def check_kb_status():
    """Check if the knowledge base is built."""
    try:
        r = requests.get(f"{API_URL}/kb-status", timeout=3)
        return r.json().get("ready", False)
    except Exception:
        return False


# ─── Sidebar: API Status ──────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔌 System Status")
    
    api_ok, health_data = check_api_health()
    
    if api_ok:
        st.success("✅ Backend API: Running")
        if health_data.get("knowledge_base_ready"):
            st.success("✅ Knowledge Base: Ready")
        else:
            st.warning("⚠️ Knowledge Base: Not Built")
    else:
        st.error("❌ Backend API: Not Running")
        st.info("Run: `cd backend && python main.py`")
    
    st.divider()
    st.markdown("**📚 How to Use:**")
    st.markdown("1. Upload support docs + HTML")
    st.markdown("2. Click 'Build Knowledge Base'")
    st.markdown("3. Enter a prompt → Generate test cases")
    st.markdown("4. Select a test case → Generate Selenium script")


# ─── Phase 1: Knowledge Base ──────────────────────────────────────────────────
st.header("📚 Phase 1: Build Knowledge Base")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Upload Support Documents + checkout.html",
        type=["md", "txt", "json", "pdf", "html", "htm"],
        accept_multiple_files=True,
        help="Upload: product_specs.md, ui_ux_guide.txt, api_endpoints.json, checkout.html, etc."
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} file(s) selected: {', '.join([f.name for f in uploaded_files])}")

with col2:
    build_btn = st.button("🧠 Build Knowledge Base", type="primary", disabled=not uploaded_files)

if build_btn and uploaded_files:
    with st.spinner("🔄 Processing documents and building knowledge base... (this may take 1-2 minutes)"):
        files_data = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
        
        try:
            response = requests.post(
                f"{API_URL}/build-knowledge-base",
                files=files_data,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                st.markdown(f"""
<div class="success-box">
✅ <strong>Knowledge Base Built Successfully!</strong><br>
📄 Documents processed: {result.get('total_documents', 0)}<br>
🧩 Total chunks created: {result.get('total_chunks', 0)}<br>
{result.get('message', '')}
</div>""", unsafe_allow_html=True)
                st.balloons()
            else:
                st.error(f"❌ Error: {response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Make sure it's running on port 8000.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()


# ─── Phase 2: Generate Test Cases ─────────────────────────────────────────────
st.header("🧪 Phase 2: Generate Test Cases")

kb_ready = check_kb_status()

if not kb_ready:
    st.warning("⚠️ Please build the knowledge base first (Phase 1).")
else:
    prompt_col, btn_col = st.columns([3, 1])
    
    with prompt_col:
        test_prompt = st.text_input(
            "What test cases would you like to generate?",
            placeholder="e.g., Generate all positive and negative test cases for the discount code feature",
            help="Be specific! Examples: 'test cases for form validation', 'test cases for shipping methods'"
        )
    
    with btn_col:
        st.write("")  # spacing
        generate_btn = st.button("🚀 Generate Test Cases", type="primary")
    
    # Quick prompt suggestions
    st.markdown("**💡 Quick Prompts:**")
    suggestion_cols = st.columns(4)
    suggestions = [
        "Generate all test cases for the discount code feature",
        "Generate test cases for form validation",
        "Generate test cases for shipping method selection",
        "Generate all test cases for the payment flow"
    ]
    
    for i, (col, suggestion) in enumerate(zip(suggestion_cols, suggestions)):
        with col:
            if st.button(f"📝 {suggestion[:30]}...", key=f"suggest_{i}"):
                test_prompt = suggestion
                st.session_state["test_prompt"] = suggestion
    
    # Use session state prompt if set
    if "test_prompt" in st.session_state and not test_prompt:
        test_prompt = st.session_state["test_prompt"]
    
    if generate_btn and test_prompt:
        with st.spinner(f"🤖 AI is generating test cases for: '{test_prompt}'..."):
            try:
                response = requests.post(
                    f"{API_URL}/generate-test-cases",
                    json={"prompt": test_prompt},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get("status") == "success":
                        test_cases = result.get("test_cases", [])
                        st.session_state["test_cases"] = test_cases
                        
                        st.success(f"✅ Generated {len(test_cases)} test cases!")
                        
                        if result.get("context_used"):
                            st.info(f"📚 Grounded in: {', '.join(set(result['context_used']))}")
                        
                        # Display test cases
                        for tc in test_cases:
                            badge = "🟢" if tc.get("test_type") == "Positive" else "🔴"
                            with st.expander(f"{badge} {tc.get('test_id', 'TC')} — {tc.get('test_scenario', 'Test Case')[:70]}"):
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.markdown(f"**Feature:** {tc.get('feature', 'N/A')}")
                                    st.markdown(f"**Type:** {tc.get('test_type', 'N/A')}")
                                    st.markdown(f"**📌 Grounded In:** `{tc.get('grounded_in', 'N/A')}`")
                                with col_b:
                                    st.markdown(f"**Expected Result:** {tc.get('expected_result', 'N/A')}")
                                    st.markdown(f"**Preconditions:** {tc.get('preconditions', 'None')}")
                                
                                if tc.get("test_steps"):
                                    st.markdown("**Test Steps:**")
                                    for j, step in enumerate(tc["test_steps"], 1):
                                        st.markdown(f"  {j}. {step}")
                        
                        # Show raw JSON
                        with st.expander("📋 View Raw JSON"):
                            st.json(test_cases)
                    
                    else:
                        st.warning("⚠️ Partial result:")
                        st.text(result.get("raw_output", "No output"))
                
                else:
                    st.error(f"❌ Error: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running. Start it with: `cd backend && python main.py`")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.divider()


# ─── Phase 3: Generate Selenium Script ────────────────────────────────────────
st.header("🔧 Phase 3: Generate Selenium Script")

if not kb_ready:
    st.warning("⚠️ Please build the knowledge base first.")
elif "test_cases" not in st.session_state or not st.session_state["test_cases"]:
    st.warning("⚠️ Please generate test cases first (Phase 2).")
else:
    test_cases = st.session_state["test_cases"]
    
    # Dropdown to select a test case
    tc_options = {
        f"{tc.get('test_id', 'TC')} — {tc.get('test_scenario', '')[:60]}": tc
        for tc in test_cases
    }
    
    selected_label = st.selectbox(
        "Select a Test Case to convert to Selenium Script:",
        options=list(tc_options.keys())
    )
    
    selected_tc = tc_options[selected_label]
    
    # Show selected test case summary
    with st.expander("📋 Selected Test Case Details"):
        st.json(selected_tc)
    
    # Optional HTML upload (if not already in KB)
    html_upload = st.file_uploader(
        "📄 Upload checkout.html (optional if already in knowledge base)",
        type=["html", "htm"],
        key="html_for_selenium"
    )
    
    script_btn = st.button("⚙️ Generate Selenium Script", type="primary")
    
    if script_btn:
        html_content = ""
        if html_upload:
            html_content = html_upload.getvalue().decode("utf-8")
        
        with st.spinner(f"🤖 Generating Selenium script for: {selected_tc.get('test_id')}..."):
            try:
                response = requests.post(
                    f"{API_URL}/generate-selenium-script",
                    json={
                        "test_case": selected_tc,
                        "html_content": html_content if html_content else None
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    script = result.get("script", "")
                    
                    st.success(f"✅ Selenium script generated for {result.get('test_id')}!")
                    
                    # Display the script in a code block
                    st.markdown("### 🐍 Generated Python Selenium Script")
                    st.code(script, language="python")
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Script",
                        data=script,
                        file_name=f"test_{selected_tc.get('test_id', 'TC001').lower().replace('-','_')}.py",
                        mime="text/plain"
                    )
                    
                    # How to run instructions
                    with st.expander("▶️ How to Run This Script"):
                        st.markdown("""
**Prerequisites:**
```bash
pip install selenium webdriver-manager
```

**Run the script:**
```bash
python test_tc001.py
```

**Note:** Chrome browser must be installed. 
The script uses `webdriver_manager` to automatically download the correct ChromeDriver.
""")
                
                else:
                    st.error(f"❌ Error: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center>🤖 QA Agent | Built with FastAPI + Streamlit + Groq AI + ChromaDB</center>",
    unsafe_allow_html=True
)
```

---

## STEP 8: Create the README

### `README.md`
```markdown
# 🤖 Autonomous QA Agent

An intelligent QA agent that builds a "testing brain" from project documentation and generates comprehensive test cases and Selenium automation scripts.

## 🛠️ Tech Stack
- **Backend:** FastAPI + Uvicorn
- **Frontend:** Streamlit
- **AI/LLM:** Groq API (LLaMA 3 70B) — free tier
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
```

---

## STEP 9: Run the Project

### 9.1 Start the Backend
Open **Terminal 1** in VS Code:
```bash
# Make sure your virtual env is active: source venv/bin/activate
cd backend
python main.py
```
You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Visit http://localhost:8000/docs to see the interactive API documentation (Swagger UI).

### 9.2 Start the Frontend
Open **Terminal 2** in VS Code (`+` button in terminal panel):
```bash
# Make sure your virtual env is active
cd frontend
streamlit run app.py
```
A browser window will open at http://localhost:8501

### 9.3 Use the App
1. **Upload files:** Click "Upload Support Documents" → select all files from the `assets/` folder
2. **Build KB:** Click "🧠 Build Knowledge Base" → wait ~1-2 minutes
3. **Generate tests:** Type "Generate all positive and negative test cases for the discount code feature" → click Generate
4. **Get Selenium script:** Pick a test case from the dropdown → click "⚙️ Generate Selenium Script"

---

## STEP 10: Push to GitHub

```bash
# From your project root
git add .
git commit -m "Initial project setup: QA Agent with FastAPI, Streamlit, and Groq"
git push origin main
```

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: groq` | Package not installed | `pip install groq` |
| `ConnectionError: localhost:8000` | Backend not started | Run `python main.py` in backend/ |
| `GROQ_API_KEY not found` | .env missing or wrong path | Check `.env` file is in project root |
| `Collection not found` | KB not built | Click "Build Knowledge Base" first |
| Slow embedding generation | First run downloads model | Wait 2-3 min, model downloads once |
| ChromaDB error on Windows | Path issue | Run from project root, not backend/ |

---

## 📚 Useful Documentation Links

- FastAPI docs: https://fastapi.tiangolo.com
- Streamlit docs: https://docs.streamlit.io
- ChromaDB docs: https://docs.trychroma.com
- Groq API docs: https://console.groq.com/docs
- sentence-transformers: https://www.sbert.net
- Selenium Python docs: https://selenium-python.readthedocs.io
- LangChain text splitters: https://python.langchain.com/docs/modules/data_connection/document_transformers/
```
