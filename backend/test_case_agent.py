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
