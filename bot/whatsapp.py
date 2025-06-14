from flask import Flask
from bot.routes import bp

# Inicializando o objeto flask e adionando as rotas
app = Flask(__name__)
app.register_blueprint(bp)