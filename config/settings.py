import os
from dotenv import load_dotenv

load_dotenv()

# Porta do servidor e sinalizacao de debug para o Flask 
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "false").lower()

# Geminic Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")