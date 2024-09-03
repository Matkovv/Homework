from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Konto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Integer, nullable=False)

class Produkt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    cena = db.Column(db.Integer, nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)

class HistoriaOperacji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typ_operacji = db.Column(db.String(50), nullable=False)
    opis = db.Column(db.String(200), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
