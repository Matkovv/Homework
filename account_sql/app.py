from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Konto, Produkt, HistoriaOperacji

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    konto = Konto.query.first()
    magazyn = Produkt.query.all()
    return render_template('index.html', konto=konto.saldo if konto else 0, magazyn=magazyn)

@app.route('/zakup', methods=['POST'])
def zakup():
    produkt = request.form['produkt']
    cena = int(request.form['cena'])
    ilosc = int(request.form['ilosc'])
    # Implementacja zakupu z użyciem bazy danych
    return redirect(url_for('index'))

@app.route('/sprzedaz', methods=['POST'])
def sprzedaz():
    produkt = request.form['produkt']
    ilosc = int(request.form['ilosc'])
    # Implementacja sprzedaży z użyciem bazy danych
    return redirect(url_for('index'))

@app.route('/saldo', methods=['POST'])
def saldo():
    kwota = int(request.form['kwota'])
    # Implementacja zmiany salda z użyciem bazy danych
    return redirect(url_for('index'))

@app.route('/historia/')
@app.route('/historia/<int:line_from>/<int:line_to>/')
def historia(line_from=None, line_to=None):
    if line_from is None or line_to is None:
        historia = HistoriaOperacji.query.all()
    else:
        historia = HistoriaOperacji.query.slice(line_from, line_to).all()
    return render_template('history.html', historia=historia)

if __name__ == '__main__':
    app.run(debug=True)
