from bot.whatsapp import app
from config.settings import DEBUG, PORT
print(DEBUG)
if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)
