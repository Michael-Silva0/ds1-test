from database import db


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    registros = db.relationship("Registro", backref="categoria", lazy=True)
    

class Registro(db.Model):
    __tablename__ = "registro"
    

    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    imagem = db.Column(db.String(200), nullable=True, default='padrao.png')  # Nome do arquivo da imagem, padrão é 'padrao.png'
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)