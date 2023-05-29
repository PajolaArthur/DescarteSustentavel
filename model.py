from main import db, datetime
<<<<<<< HEAD

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Chave primária auto
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow) # Gerado no momento de insert
=======
from datetime import *

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Chave primária auto
    created = db.Column(db.DateTime, default=datetime.utcnow) # Gerado no momento de insert
>>>>>>> eb18984 (Upt_1.6)
    nome = db.Column(db.String(40), nullable = False) # admin
    senha = db.Column(db.String(40), nullable = False) # admin

class Coletas(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Chave primária auto
<<<<<<< HEAD
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow) # Gerado no momento de insert
=======
    created = db.Column(db.DateTime, default=datetime.utcnow) # Gerado no momento de insert
>>>>>>> eb18984 (Upt_1.6)
    descricao = db.Column(db.String(60), nullable = False) # Fogão
    quantidade = db.Column(db.String(3), nullable = False) # 2
    endereco = db.Column(db.String(40), nullable = False) # Praça Coronel Francisco Orlando 600
    telefone = db.Column(db.String(15), nullable = False) # 16992956535
    diacoleta = db.Column(db.String(15), nullable = True) # Segunda-Feira
    horacoleta = db.Column(db.String(5), nullable = True) # 15 Horas
    situacao = db.Column(db.String(20), nullable = False) # Em andamento