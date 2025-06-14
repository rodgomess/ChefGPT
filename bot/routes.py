
from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

import json, re
from collections import defaultdict

from ai.client import ask_gemini
from ai.prompt import PROMPT_INIT, PROMPT_FINISH

bp = Blueprint("whatsapp", __name__)

# Palavra chave de encerramento
ended_keywords = "Pedido feito com sucesso"

# Inicializando historico de conversas como dicionario
user_histories = defaultdict(list)

@bp.route("/whatsapp", methods=["POST"])
def whatsapp_reply():

    # Captura a mensagem e o numero do cliente
    user_msg = request.form.get("Body")
    user_number = request.form.get("From")


    # Adiciona mensagem do usuario ao seu respectivo historico, como cliente
    user_histories[user_number].append(f"Cliente: {user_msg}")

    # Coloca o prompt inicial com o historico de conersa para que o bot saiba oq já foi dito
    full_prompt = [PROMPT_INIT] + user_histories[user_number]

    # Envia o prompt inteiro com historico e a ultima pergunta do cliente para o bot
    bot_response = ask_gemini(full_prompt)

    # Adiciona resposta do bot ao historico, como atendente
    user_histories[user_number].append(f"Atendente: {bot_response}")

    # Envia resposta pro WhatsApp
    resp = MessagingResponse()
    resp.message(bot_response)
    
    # Quando o Bot finaliza o pedido ele envia uma palavra chave indicando que o antendimento deve ser finalizado
    if ended_keywords in bot_response:

        # Adiciona ao historico de conversas o telefone do cliente para criação do json
        user_histories[user_number].append(f"Telefone do cliente: {user_number}")

        # Coloca o prompt de fechamento para finalizar a conversa e criar o json
        full_prompt  = user_histories[user_number] + [PROMPT_FINISH]
        res_order = ask_gemini(full_prompt)

        # Remove a palavra "``json" do inicio e "```" do final e adiciona em um formato json
        clean_order = re.sub(r"^```json\s*|```$", "", res_order).strip()
        json_order = json.loads(clean_order)

        # Salva o json com todas as informações do pedido
        with open(f"orders/order_{user_number.replace('whatsapp:+', '')}.json", "w", encoding="utf-8") as f:
            json.dump(json_order, f)

        # Reseta a conversa
        user_histories.pop(user_number, None)

    return str(resp)