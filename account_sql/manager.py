import os
import json

class Manager:
    def __init__(self):
        self.konto_file = 'data/konto.txt'
        self.magazyn_file = 'data/magazyn.txt'
        self.historia_file = 'data/historia.txt'
        self.konto = self.load_konto()
        self.magazyn = self.load_magazyn()
        self.historia_operacji = self.load_historia()

    def wykonaj_zakup(self, produkt, cena, ilosc):
        koszt = cena * ilosc
        konto = Konto.query.first()

        if konto.saldo < koszt:
            print("Błąd: Brak wystarczających środków na koncie.")
            return

        produkt_db = Produkt.query.filter_by(nazwa=produkt).first()
        if produkt_db:
            produkt_db.ilosc += ilosc
        else:
            produkt_db = Produkt(nazwa=produkt, cena=cena, ilosc=ilosc)
            db.session.add(produkt_db)

        konto.saldo -= koszt
        db.session.add(konto)

        operacja = HistoriaOperacji(typ_operacji='zakup', opis=f'Zakup {ilosc} szt. {produkt} za {koszt} PLN')
        db.session.add(operacja)

        db.session.commit()

    def wykonaj_sprzedaz(self, produkt, ilosc):
        produkt_db = Produkt.query.filter_by(nazwa=produkt).first()
        if not produkt_db or produkt_db.ilosc < ilosc:
            print("Błąd: Brak wystarczającej ilości produktu w magazynie.")
            return

        przychod = produkt_db.cena * ilosc
        konto = Konto.query.first()
        konto.saldo += przychod

        produkt_db.ilosc -= ilosc
        if produkt_db.ilosc == 0:
            db.session.delete(produkt_db)
        else:
            db.session.add(produkt_db)

        db.session.add(konto)

        operacja = HistoriaOperacji(typ_operacji='sprzedaż', opis=f'Sprzedaż {ilosc} szt. {produkt} za {przychod} PLN')
        db.session.add(operacja)

        db.session.commit()

    def wykonaj_saldo(self, kwota):
        konto = Konto.query.first()
        if not konto:
            konto = Konto(saldo=0)
            db.session.add(konto)

        konto.saldo += kwota
        db.session.add(konto)

        operacja = HistoriaOperacji(typ_operacji='saldo', opis=f'Saldo zmienione o {kwota} PLN')
        db.session.add(operacja)

        db.session.commit()

    def load_konto(self):
        if os.path.exists(self.konto_file):
            with open(self.konto_file, 'r') as f:
                content = f.read().strip()
                if content:
                    try:
                        return int(content)
                    except ValueError:
                        print("Błąd: Zawartość pliku konto.txt nie jest poprawną liczbą. Ustawiam stan konta na 0.")
                        return 0
                else:
                    return 0
        return 0

    def save_konto(self):
        with open(self.konto_file, 'w') as f:
            f.write(str(self.konto))

    def load_magazyn(self):
        if os.path.exists(self.magazyn_file):
            with open(self.magazyn_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("Błąd: Plik magazyn.txt nie zawiera poprawnych danych JSON. Ustawiam pusty magazyn.")
                    return {}
        return {}

    def save_magazyn(self):
        with open(self.magazyn_file, 'w') as f:
            json.dump(self.magazyn, f)

    def load_historia(self):
        if os.path.exists(self.historia_file):
            with open(self.historia_file, 'r') as f:
                return f.read().strip().splitlines()
        return []

    def save_historia(self):
        with open(self.historia_file, 'a') as f:
            f.write("\n".join(self.historia_operacji) + "\n")
        self.historia_operacji = []

    def get_konto(self):
        return self.konto

    def get_magazyn(self):
        return self.magazyn

    def sprawdz_integralnosc():
        konto = Konto.query.first()
        if not konto:
            print("Brak konta w bazie danych.")
            return

        historia = HistoriaOperacji.query.all()
        operacje_saldo = [op for op in historia if op.typ_operacji == 'saldo']
        suma_saldo = sum(int(op.opis.split(' ')[-2]) for op in operacje_saldo)

        produkty = Produkt.query.all()
        suma_zakupow = sum(prod.cena * prod.ilosc for prod in produkty)

        if konto.saldo != suma_saldo - suma_zakupow:
            print("Błąd integralności: Saldo nie zgadza się z historią operacji.")
        else:
            print("Dane są zgodne.")
