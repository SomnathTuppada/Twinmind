import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

try:
    model = genai.GenerativeModel("gemini-pro")
    print("✓ gemini-pro model loaded")
    
    # Try a simple call
    response = model.generate_content("Hello")
    print(f"✓ Model works! Response: {response.text[:50]}...")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {str(e)}")
