class Manager:
    def __init__(self):
        self.konto = 0
        self.magazyn = {}
        self.historia_operacji = []
        self.commands = {
            "saldo": self.wykonaj_saldo,
            "sprzedaż": self.wykonaj_sprzedaz,
            "zakup": self.wykonaj_zakup,
            "konto": self.pokaz_stan_konta,
            "lista": self.pokaz_magazyn,
            "magazyn": self.pokaz_stan_produktu,
            "przegląd": self.przeglad_operacji,
            "koniec": self.koniec_programu
        }
        self.is_running = True

    def assign(self, command_name, function):
        self.commands[command_name] = function

    def execute(self, command_name, *args):
        if command_name in self.commands:
            self.commands[command_name](*args)
        else:
            print(f"Błąd: Nieznana komenda '{command_name}'.")

    def wykonaj_saldo(self, kwota):
        self.konto += kwota
        self.historia_operacji.append(f"saldo {kwota}")

    def wykonaj_sprzedaz(self, produkt, cena, ilosc):
        if produkt not in self.magazyn or self.magazyn[produkt]["ilosc"] < ilosc:
            print("Błąd: Brak wystarczającej ilości produktu w magazynie.")
            return
        self.magazyn[produkt]["ilosc"] -= ilosc
        self.konto += cena * ilosc
        self.historia_operacji.append(f"sprzedaż {produkt} {cena} {ilosc}")
        if self.magazyn[produkt]["ilosc"] == 0:
            del self.magazyn[produkt]

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
            self.magazyn[produkt]["ilosc"] += ilosc
        else:
            self.magazyn[produkt] = {"cena": cena, "ilosc": ilosc}
        self.historia_operacji.append(f"zakup {produkt} {cena} {ilosc}")

    def pokaz_stan_konta(self):
        print(f"Stan konta: {self.konto} PLN")

    def pokaz_magazyn(self):
        if not self.magazyn:
            print("Magazyn jest pusty.")
        else:
            print("Stan magazynu:")
            for produkt, dane in self.magazyn.items():
                print(f"{produkt}: {dane['ilosc']} szt. (Cena: {dane['cena']} PLN)")

    def pokaz_stan_produktu(self, produkt):
        if produkt in self.magazyn:
            print(f"{produkt}: {self.magazyn[produkt]['ilosc']} szt. (Cena: {self.magazyn[produkt]['cena']} PLN)")
        else:
            print(f"Błąd: Produkt {produkt} nie istnieje w magazynie.")

    def przeglad_operacji(self, od, do):
        if od == "":
            od = 0
        else:
            od = int(od)
        if do == "":
            do = len(self.historia_operacji)
        else:
            do = int(do)

        if od < 0 or do > len(self.historia_operacji) or od >= do:
            print(f"Błąd: Zakres niepoprawny. Aktualna liczba operacji: {len(self.historia_operacji)}")
            return

        for i in range(od, do):
            print(f"{i}: {self.historia_operacji[i]}")

    def koniec_programu(self):
        print("Zakończenie programu.")
        self.is_running = False

    def pokaz_komendy(self):
        print("\nDostępne komendy:")
        for komenda in self.commands.keys():
            print(komenda)


def main():
    manager = Manager()

    while manager.is_running:
        manager.pokaz_komendy()
        komenda = input("Wprowadź komendę: ").strip().lower()

        if komenda == "saldo":
            try:
                kwota = int(input("Podaj kwotę do dodania/odjęcia: "))
                manager.execute(komenda, kwota)
            except ValueError:
                print("Błąd: Podaj prawidłową kwotę.")

        elif komenda == "sprzedaż":
            produkt = input("Podaj nazwę produktu: ").strip()
            try:
                cena = int(input("Podaj cenę produktu: "))
                ilosc = int(input("Podaj liczbę sztuk: "))
                manager.execute(komenda, produkt, cena, ilosc)
            except ValueError:
                print("Błąd: Podaj prawidłową cenę i ilość.")

        elif komenda == "zakup":
            produkt = input("Podaj nazwę produktu: ").strip()
            try:
                cena = int(input("Podaj cenę produktu: "))
                ilosc = int(input("Podaj liczbę sztuk: "))
                manager.execute(komenda, produkt, cena, ilosc)
            except ValueError:
                print("Błąd: Podaj prawidłową cenę i ilość.")

        elif komenda in ["konto", "lista", "koniec"]:
            manager.execute(komenda)

        elif komenda == "magazyn":
            produkt = input("Podaj nazwę produktu: ").strip()
            manager.execute(komenda, produkt)

        elif komenda == "przegląd":
            od = input("Podaj indeks początkowy (lub naciśnij Enter dla początku): ").strip()
            do = input("Podaj indeks końcowy (lub naciśnij Enter dla końca): ").strip()
            manager.execute(komenda, od, do)

        else:
            print("Błąd: Nieznana komenda.")


if __name__ == "__main__":
    main()
