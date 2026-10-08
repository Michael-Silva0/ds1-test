import os

from flask import Flask

from database import db
from routes import main_bp

# inicializa o servidor web da aplicação flask
app = Flask(__name__)

# Configurações do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["SECRET_KEY"] = "chave_secreta_etec_ds1_2026"
app.config["MAX_CONTENT_LENGTH"] = (
    5 * 1024 * 1024
)  # Limite de tamanho do arquivo (5 MB)
# Lista global para armazenar os dicionários dos cadastros


# Inicializa o banco de dados com a aplicação Flask
db.init_app(app)
app.register_blueprint(main_bp)

# Cria as tabelas do banco de dados se elas não existirem
with app.app_context():
    os.makedirs(
        app.config["UPLOAD_FOLDER"], exist_ok=True
    )  # Cria a pasta de uploads se não existir
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
