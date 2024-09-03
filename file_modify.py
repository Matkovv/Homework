import sys
import csv
import json
import pickle
from abc import ABC, abstractmethod


class FileHandler(ABC):
    def __init__(self, filename):
        self.filename = filename
        self.data = None

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, output_filename):
        pass

    def apply_changes(self, changes):
        for change in changes:
            x, y, value = map(str.strip, change.split(','))
            x, y = int(x), int(y)
            self.data[y][x] = value


class CSVHandler(FileHandler):
    def load(self):
        with open(self.filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            self.data = [row for row in reader]

    def save(self, output_filename):
        with open(output_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)


class JSONHandler(FileHandler):
    def load(self):
        with open(self.filename, mode='r') as file:
            self.data = json.load(file)

    def save(self, output_filename):
        with open(output_filename, mode='w') as file:
            json.dump(self.data, file, indent=4)


class TXTHHandler(FileHandler):
    def load(self):
        with open(self.filename, mode='r') as file:
            self.data = [line.strip().split(',') for line in file.readlines()]

    def save(self, output_filename):
        with open(output_filename, mode='w') as file:
            for row in self.data:
                file.write(','.join(row) + '\n')


class PickleHandler(FileHandler):
    def load(self):
        with open(self.filename, mode='rb') as file:
            self.data = pickle.load(file)

    def save(self, output_filename):
        with open(output_filename, mode='wb') as file:
            pickle.dump(self.data, file)


class FileHandlerFactory:
    @staticmethod
    def get_handler(filename):
        if filename.endswith('.csv'):
            return CSVHandler(filename)
        elif filename.endswith('.json'):
            return JSONHandler(filename)
        elif filename.endswith('.txt'):
            return TXTHHandler(filename)
        elif filename.endswith('.pickle'):
            return PickleHandler(filename)
        else:
            raise ValueError("Unsupported file format!")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python reader.py <input_file> <output_file> <change_1> <change_2> ... <change_n>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    changes = sys.argv[3:]

    handler = FileHandlerFactory.get_handler(input_file)
    handler.load()
    handler.apply_changes(changes)

    # Wyświetl zmodyfikowaną zawartość
    for row in handler.data:
        print(','.join(row))

    # Zapisz zmodyfikowaną zawartość do pliku wyjściowego
    handler.save(output_file)
