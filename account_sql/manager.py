from models import db, Konto, Produkt, HistoriaOperacji


class Manager:
    def __init__(self):
        pass

    def get_konto(self):
        konto = Konto.query.first()
        if konto:
            return konto.saldo
        else:
            return 0

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
