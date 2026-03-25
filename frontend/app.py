import json
import os
import streamlit as st
import requests

# FastAPI backend URL - read from Streamlit secrets (production) or environment (development)
try:
    API_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://localhost:8000"))
except (KeyError, FileNotFoundError, Exception):
    # Fallback if secrets.toml doesn't exist (local development)
    API_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

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
