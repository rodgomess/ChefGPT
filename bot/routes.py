from ai.client import ask_gemini
from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from ai.prompt import PROMPT_INIT, PROMPT_FINISH
import json

bp = Blueprint("whatsapp", __name__)

ended_keywords = "Pedido feito com sucesso"
user_histories = {}

@bp.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    user_msg = request.form.get("Body")
    user_number = request.form.get("From")

    # Inicializa histórico
    if user_number not in user_histories:
        user_histories[user_number] = [f"Cliente: {user_msg}"]
    else:
        user_histories[user_number].append(f'Cliente: {user_msg}')

    full_prompt = [PROMPT_INIT] + user_histories[user_number]
    
    res_gemini = ask_gemini(full_prompt)

    # Adiciona resposta ao histórico
    user_histories[user_number].append(f"Atendente: {res_gemini}")

    # Envia resposta pro WhatsApp
    response = MessagingResponse()
    response.message(res_gemini)
    
    if ended_keywords in res_gemini:
        add_client_tel = f"Telefone do cliente: {user_number}"
        full_prompt  = user_histories[user_number] + [add_client_tel] + [PROMPT_FINISH]
        
        str_order = ask_gemini(full_prompt)

        # Remove a palavra "json" se estiver no início
        if str_order.lower().startswith("```json"):
            str_order = str_order[8:-4].strip()

        json_order = json.loads(str_order)

        with open(f"orders/order_{user_number.replace(':', '')}.json", "w", encoding="utf-8") as file:
            json.dump(json_order, file)

        # Reseta conversa
        del user_histories[user_number]
    return str(response)