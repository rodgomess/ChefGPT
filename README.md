# 🍔 ChefGPT

Bot de autoatendimento para restaurantes via WhatsApp, com inteligência artificial para conversas humanizadas.

## 🚀 Visão Geral

ChefGPT é uma solução completa de atendimento automatizado para restaurantes, que utiliza:
 - Flask para servidor web e webhook de mensagens.
 - Twilio API para integração com WhatsApp.
 - Google Gemini (GenAI SDK) para geração de respostas inteligentes e análise de pedidos.
 - Estrutura modular que separa configurações, lógica de IA, rotas do bot e armazenamento de pedidos.

O fluxo principal é:
1. O cliente envia uma mensagem pelo WhatsApp.
2. O servidor Flask recebe o webhook e encaminha a mensagem à IA.
3. A IA (Gemini) responde e o servidor envia de volta via Twilio.
4. O bot anota itens, endereço e forma de pagamento.
Quando o pedido é finalizado, gera um JSON e salva em orders/.

## ⭐ Funcionalidades
 - Atendimento conversacional, sugerindo itens com base em um cardápio (menu.json).
 - Coleta de dados do pedido: itens, quantidades, observações, endereço e pagamento.
 - Detecta fim de pedido e exporta estrutura JSON.
 - Arquitetura modular, facilitando manutenção e extensão.

## 🏗️ Arquitetura e Stack

 - **Backend Framework**: Flask
 - **Comunicação**: Twilio WhatsApp Sandbox
 - **IA:** Google Gemini (GenAI SDK)
 - **Configuração**: python-dotenv

**Estrutura de Pastas:**
 ```bash
ChefGPT/
├── ai/                 # Lógica e templates de IA
│   ├── client.py       # Wrapper para chamadas ao Gemini
│   └── prompts.py      # Templates de prompt para conversas e JSON
├── bot/                # Módulo Flask e integração com Twilio
│   ├── routes.py       # Blueprint das rotas de WhatsApp
│   └── whatsapp.py     # Registra blueprint no app
├── config/             # Variáveis de ambiente e settings
│   └── settings.py     # Carrega chaves e configurações
├── orders/             # Pedidos finalizados em JSON (contém .gitkeep)
├── menu.json           # Cardápio usado pela IA
├── run.py              # Entry point da aplicação
├── requirements.txt    # Dependências Python
├── .env.example        # Exemplo de variáveis de ambiente
└── .gitignore          # Arquivos ignorados pelo Git
```

## ⚙️ Como Rodar Localmente

**Pré-requisitos**
 - Python 3.10+
 - Conta Twilio (sandbox WhatsApp) com credenciais
 - API Key do Google Gemini
 - ngrok (para expor o servidor local)

**Passos**
1. Clone o repositório:
    ```
    git clone https://github.com/SEU_USUARIO/ChefGPT.git
    cd ChefGPT
    ```

2. instale dependências:
    ```
    pip install -r requirements.txt
    ```

3. Configure variáveis de ambiente:
   - Copie .env.example para .env
   - Preencha:

        ```
        GEMINI_API_KEY=...
        TWILIO_ACCOUNT_SID=...
        TWILIO_AUTH_TOKEN=...
        TWILIO_NUMBER=whatsapp:+14155238886
        FLASK_DEBUG=true
        ```

4. Inicie o servidor Flask:
    
    ```
    python run.py
    ```

5. Em outro terminal, exponha a porta com ngrok:
    
    ```
    ngrok http 5000
    ```

6. No console do Twilio Sandbox, defina o webhook para:
    
    ```
    https://<NGROK_ID>.ngrok.io/whatsapp
    ```

7. Siga os passos da Twilio para logar no chat


## 🧑‍💻 Autor
Rodrigo Gomes
🔗 [LinkedIn](https://www.linkedin.com/in/rodrigogomes-profile/)
