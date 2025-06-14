from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from google import genai
from dotenv import load_dotenv
import json
import os


# Secrets 
load_dotenv()
# Gemini key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

with open('menu.json', 'r') as file:
    menu_json = json.load(file)
menu = json.dumps(menu_json, ensure_ascii=False, indent=2)

prompt_init = {
f"""
Você é um atendente virtual de um restaurante que conversa com os clientes pelo WhatsApp.  
Seja educado, objetivo e claro nas respostas.

Seu papel é:
- Ajudar o cliente a montar um pedido completo
- Sugerir itens do cardápio com base no que o cliente quer
- Responder com base **exclusivamente no cardápio fornecido**
OBS: nao precisa enviar "Atendente:" no começo da frase

Durante a conversa:
- Anote todos os itens que o cliente pedir, incluindo acompanhamentos e bebidas
- Anote informações de pagamento se o cliente não tiver dito ainda, para isso informe o valor total do pedido e pergunte a forma de pagamento.
- Anote o endereço de envio do pedido caso o cliente não tenha dito ainda na conversa.
- Aguarde o cliente dizer que **terminou o pedido**, com frases como:  
  "só isso", "pode fechar", "só isso mesmo", "pode finalizar", "nada mais", etc.
Se o cliente pedir algo fora do cardápio, avise com educação e sugira algo semelhante.

Quando finalizar e conseguir todas as informações faça esses passos
2. Resuma claramente o pedido com:
   - Nome dos itens
   - Preço individual
   - Total do pedido
   - Endereço
   - Forma de pagamento
3. Finalize a conversa com unicamente "Pedido feito com sucesso", para o codigo finalizar a conversa e gravar o pedido

{menu}
"""
}

prompt_finish = {
"""
Coloque todos os items do pedido dentro desse formato simples como no exemplo 
{
  "telefone_cliente": "+5511999999999",
  "endereco_entrega": "Rua Exemplo 123 Apartamento 202",
  "forma_pagamento": "Pix",
  "itens": [
    {
      "nome": "Cheeseburger",
      "quantidade": 2,
      "preco_unitario": 20.00,
      "observacoes": "sem cebola"
    },
    {
      "nome": "Pepsi",
      "quantidade": 1,
      "preco_unitario": 5.00,
      "observacoes": ""
    }
  ],
  "valor_total": 45.00
}
Mande na mensagem apenas as informações nesse formato em texto
"""
}

ended_keywords = "Pedido feito com sucesso"

user_histories = {}

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    user_msg = request.form.get("Body")
    user_number = request.form.get("From")

    if user_number not in user_histories:
        user_histories[user_number] = [f"Cliente: {user_msg}"]
    else:
        user_histories[user_number].append(f'Cliente: {user_msg}')

    full_prompt = [prompt_init] + user_histories[user_number]
    
    res_gemini = client.models.generate_content(model="gemini-2.0-flash", contents=full_prompt).text.strip()

    # Adiciona resposta ao histórico
    user_histories[user_number].append(f"Atendente: {res_gemini}")

    # Envia resposta pro WhatsApp
    response = MessagingResponse()
    response.message(res_gemini)
    
    if ended_keywords in res_gemini:
        add_client_tel = f"Telefone do cliente: {user_number}"
        full_prompt  = user_histories[user_number] + [add_client_tel] + [prompt_finish]
        str_order = client.models.generate_content(model="gemini-2.0-flash", contents=full_prompt).text.strip()

        # Remove a palavra "json" se estiver no início
        if str_order.lower().startswith("```json"):
            str_order = str_order[8:-4].strip()

        json_order = json.loads(str_order)

        with open(f"orders/order_{user_number.replace(':', '')}.json", "w", encoding="utf-8") as file:
            json.dump(json_order, file)

        # Reseta conversa
        del user_histories[user_number]
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)