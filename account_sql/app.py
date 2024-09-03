from flask import Flask, render_template, request, redirect, url_for
from manager import Manager
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firma.db'  # Ścieżka do pliku bazy danych
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app = Flask(__name__)
manager = Manager()
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html',
                           konto=manager.get_konto(),
                           magazyn=manager.get_magazyn())

@app.route('/zakup', methods=['POST'])
def zakup():
    produkt = request.form['produkt']
    cena = int(request.form['cena'])
    ilosc = int(request.form['ilosc'])
    manager.wykonaj_zakup(produkt, cena, ilosc)
    return redirect(url_for('index'))

@app.route('/sprzedaz', methods=['POST'])
def sprzedaz():
    produkt = request.form['produkt']
    ilosc = int(request.form['ilosc'])
    manager.wykonaj_sprzedaz(produkt, ilosc)
    return redirect(url_for('index'))

@app.route('/saldo', methods=['POST'])
def saldo():
    kwota = int(request.form['kwota'])
    manager.wykonaj_saldo(kwota)
    return redirect(url_for('index'))

@app.route('/historia/')
@app.route('/historia/<int:line_from>/<int:line_to>/')
def historia(line_from=None, line_to=None):
    historia, error = manager.get_historia(line_from, line_to)
    return render_template('history.html', historia=historia, error=error)

if __name__ == '__main__':
    app.run(debug=True)
