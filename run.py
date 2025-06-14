from bot.whatsapp import app
from config.settings import DEBUG, PORT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)