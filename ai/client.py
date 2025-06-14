from google import genai
import json

from config.settings import GEMINI_API_KEY

_model = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(contents, model_name="gemini-2.0-flash"):
    """
    Envia um conteudo e obtem uma resposta do Gemini
    
    parms
        contents: Pergunta a ser feita para IA
        model_name: Modelo da IA
    
    return
        response: resposta elaborada pelo Gemini
    """
    response = _model.models.generate_content(model="gemini-2.0-flash", contents=contents)
    return response.text.strip()