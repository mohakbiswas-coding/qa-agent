# backend/selenium_agent.py
import os
import re
from typing import Dict, Any

from groq import Groq
from dotenv import load_dotenv
from knowledge_base import retrieve_relevant_chunks

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


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
