import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Setup Client
api_key = os.getenv("GEMINI_API_KEY")
client = None

if api_key:
    client = genai.Client(api_key=api_key)

def ask_ai_for_fix(code_content, issues_list):
    """
    Sends the code and the list of static analysis errors to Gemini.
    Returns a refactored version or advice.
    """
    if not client:
        return "❌ Error: No API Key found in .env file."

    # Turn the list of dicts into a string
    issues_text = ""
    for issue in issues_list:
        issues_text += f"- Line {issue['line']}: {issue['message']}\n"

    prompt = f"""
    You are a Senior Python Developer. I ran a static analysis tool on this code and found these issues:
    
    {issues_text}
    
    Here is the original code:
    ```python
    {code_content}
    ```
    
    Please provide:
    1. A short explanation of how to fix the "Bloat" (Long Function).
    2. A REFACTORED version of the code that splits the logic into smaller functions or fixes the imports.
    Keep the explanation brief. Focus on the code.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", # Or gemini-1.5-flash
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error contacting AI: {e}"