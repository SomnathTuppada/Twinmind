from google.generativeai import GenerativeModel, configure
from app.config import settings

# Configure API key (REST client only)
configure(api_key=settings.GEMINI_API_KEY)

# Use gemini-2.0-flash model which is available
model = GenerativeModel("gemini-2.0-flash")

def ask_gemini(context, question):
    prompt = f"""Use ONLY the context below to answer the user's question.

---CONTEXT---
{context}
------------

QUESTION: {question}

If the answer is not present in the context, respond with:
"Not found in context."
"""

    # REST-ONLY generate content
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini error: {str(e)}")
        raise
