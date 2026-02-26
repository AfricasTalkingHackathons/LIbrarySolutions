import os
import importlib
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    try:
        genai = importlib.import_module("google.genai")
    except ImportError as exc:
        raise ImportError(
            "Gemini SDK not found. Install 'google-genai' in the active environment."
        ) from exc

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Tell me a short joke about programming."
)

print(response.text)