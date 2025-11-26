from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    pergunta = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    respondida = db.Column(db.Boolean, default=False)
    resposta = db.Column(db.Text)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    autor = db.Column(db.String(100), default='Admin')