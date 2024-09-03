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
        if koszt > self.konto:
            print("Błąd: Brak wystarczających środków na koncie.")
            return
        if ilosc <= 0 or cena <= 0:
            print("Błąd: Cena i ilość muszą być dodatnie.")
            return
        self.konto -= koszt
        if produkt in self.magazyn:
            self.magazyn[produkt]['ilosc'] += ilosc
        else:
            self.magazyn[produkt] = {'cena': cena, 'ilosc': ilosc}
        self.historia_operacji.append(f"zakup {produkt} {cena} {ilosc}")
        self.save_magazyn()
        self.save_konto()
        self.save_historia()

    def wykonaj_sprzedaz(self, produkt, ilosc):
        if produkt not in self.magazyn or self.magazyn[produkt]['ilosc'] < ilosc:
            print("Błąd: Brak wystarczającej ilości produktu w magazynie.")
            return
        self.magazyn[produkt]['ilosc'] -= ilosc
        self.konto += self.magazyn[produkt]['cena'] * ilosc
        self.historia_operacji.append(f"sprzedaż {produkt} {self.magazyn[produkt]['cena']} {ilosc}")
        if self.magazyn[produkt]['ilosc'] == 0:
            del self.magazyn[produkt]
        self.save_magazyn()
        self.save_konto()
        self.save_historia()

    def wykonaj_saldo(self, kwota):
        self.konto += kwota
        self.historia_operacji.append(f"saldo {kwota}")
        self.save_konto()
        self.save_historia()

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

    # Dodaj inne metody do zarządzania operacjami jak zakup, sprzedaż itp.
