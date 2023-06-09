from main import db, datetime
from datetime import *

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Chave primária auto
    created = db.Column(db.DateTime, default=datetime.now) # Gerado no momento de insert
    nome = db.Column(db.String(40), nullable = False) # admin
    senha = db.Column(db.String(40), nullable = False) # admin

class Coletas(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Chave primária auto
    created = db.Column(db.DateTime, default=datetime.now) # Gerado no momento de insert
    descricao = db.Column(db.String(60), nullable = False) # Fogão
    quantidade = db.Column(db.String(3), nullable = False) # 2
    endereco = db.Column(db.String(40), nullable = False) # Praça Coronel Francisco Orlando 600
    telefone = db.Column(db.String(15), nullable = False) # 16992956535
    diacoleta = db.Column(db.String(15), nullable = True) # Segunda-Feira
    horacoleta = db.Column(db.String(5), nullable = True) # 15 Horas
    situacao = db.Column(db.String(20), nullable = False) # Em andamento
