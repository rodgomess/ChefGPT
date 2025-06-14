import os
from dotenv import load_dotenv

load_dotenv()

# Flask
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "false").lower()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")