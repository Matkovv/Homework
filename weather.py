import json
from datetime import datetime


class WeatherForecast:
    def __init__(self, file_path=None):
        self._forecasts = {}
        self.file_path = file_path
        if file_path:
            self._load_from_file(file_path)

    def _load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self._forecasts = json.load(f)
            self._forecasts = {datetime.strptime(k, '%Y-%m-%d'): v for k, v in self._forecasts.items()}
        except FileNotFoundError:
            print(f"File {file_path} not found, starting with an empty forecast.")

    def save_to_file(self, file_path=None):
        if file_path:
            self.file_path = file_path
        if not self.file_path:
            raise ValueError("File path must be specified to save the forecast.")

        forecasts_to_save = {k.strftime('%Y-%m-%d'): v for k, v in self._forecasts.items()}

        with open(self.file_path, 'w') as f:
            json.dump(forecasts_to_save, f)

    def __setitem__(self, date, weather):
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        self._forecasts[date] = weather

    def __getitem__(self, date):
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        return self._forecasts.get(date, None)

    def __iter__(self):
        return iter(self._forecasts)

    def items(self):
        return self._forecasts.items()

    def query_api(self, date):

        simulated_response = {
            'temperature': 20,
            'description': 'Clear sky',
            'wind_speed': 5
        }
        self[date] = simulated_response
        return simulated_response
