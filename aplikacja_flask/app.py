from flask import Flask, render_template, request, redirect, url_for
from manager import Manager

app = Flask(__name__)
manager = Manager()

@app.route('/')
def index():
    return render_template('index.html',
                           konto=manager.konto,
                           magazyn=manager.magazyn)

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
    cena = int(request.form['cena'])
    ilosc = int(request.form['ilosc'])
    manager.wykonaj_sprzedaz(produkt, cena, ilosc)
    return redirect(url_for('index'))

@app.route('/saldo', methods=['POST'])
def saldo():
    kwota = int(request.form['kwota'])
    manager.wykonaj_saldo(kwota)
    return redirect(url_for('index'))

@app.route('/historia/')
@app.route('/historia/<int:line_from>/<int:line_to>/')
def historia(line_from=None, line_to=None):
    if line_from is None or line_to is None:
        historia = manager.historia_operacji
    else:
        historia = manager.historia_operacji[line_from:line_to]
    return render_template('history.html', historia=historia)

if __name__ == '__main__':
    app.run(debug=True)
