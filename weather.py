import json
import requests
from datetime import date


class Spots:
    """
    Объект Spots хранит в себе список мест
    """
    def __init__(self, json_file):
        """
        Принимает имя файла, открывает его и читает оттуда словарь с именами и координатами
        имеет два атрибута - имя файла и сохраненный словарь
        """
        self.json_file = json_file
        with open(self.json_file, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
        self.spots = data

    def all_spots_names(self):
        """
        Возвращает список мест, берет ключи из словаря (имена мест)
        """
        return [spot for spot in self.spots]

    def spot_coord(self, spot):
        """
        Принимает имя места, и если оно есть в списке self.spots возвращает его координаты
        """
        if spot in self.spots:
            return self.spots[spot]

    def data_write(self):
        with open(self.json_file, "w", encoding="utf-8") as file:
            json.dump(self.spots, file, ensure_ascii=False)

    def add_spot(self, spot_name, spot_coord):
        spot_coord = f"latitude={spot_coord[:5]}&longitude={spot_coord[6:]}"
        self.spots[spot_name] = spot_coord
        self.data_write()

    def del_spot(self, spot_name):
        del self.spots[spot_name]


class Weather:
    def __init__(self, coord, spot_name):
        self.coord = coord
        self.spot_name = spot_name

    def weather(self):
        cur_date = date.today()
        answer = self.request_for_api(cur_date)
        answer = f"Погода {self.spot_name}\n" \
                 f"{cur_date}" \
                 f"\n\n" \
                 f"Сейчас:\n" \
                 f"Температура: {answer['current_weather']['temperature']}°C\n" \
                 f"Ветер: {Wind(answer['current_weather']['windspeed'], answer['current_weather']['winddirection'])}" \
                 f"\n\n" \
                 f"10:00\n" \
                 f"Температура: {answer['hourly']['temperature_2m'][10]}°C\n" \
                 f"Ветер: {Wind(answer['hourly']['windspeed_10m'][10], answer['hourly']['winddirection_10m'][10], answer['hourly']['windgusts_10m'][10])}" \
                 f"\n\n" \
                 f"12:00\n" \
                 f"Температура: {answer['hourly']['temperature_2m'][12]}°C\n" \
                 f"Ветер: {Wind(answer['hourly']['windspeed_10m'][12], answer['hourly']['winddirection_10m'][12], answer['hourly']['windgusts_10m'][12])}" \
                 f"\n\n" \
                 f"14:00\n" \
                 f"Температура: {answer['hourly']['temperature_2m'][14]}°C\n" \
                 f"Ветер: {Wind(answer['hourly']['windspeed_10m'][14], answer['hourly']['winddirection_10m'][14], answer['hourly']['windgusts_10m'][14])}" \
                 f"\n\n" \
                 f"16:00\n" \
                 f"Температура: {answer['hourly']['temperature_2m'][16]}°C\n" \
                 f"Ветер: {Wind(answer['hourly']['windspeed_10m'][16], answer['hourly']['winddirection_10m'][16], answer['hourly']['windgusts_10m'][16])}"
        return answer

    def request_for_api(self, cur_date):
        req = f"https://api.open-meteo.com/v1/forecast?{self.coord}&hourly=temperature_2m,windspeed_10m," \
              f"windgusts_10m,winddirection_10m&windspeed_unit=ms&timezone=auto&start_date={cur_date}&end_date={cur_date}" \
              f"&current_weather=true"
        answer = requests.get(req)
        answer = json.loads(answer.text)
        return answer


class Wind:
    def __init__(self, speed, direction, gusts=None):
        self.speed = str(float(round(speed, 1)))
        self.direction = self.direction_str(direction)
        self.gusts = gusts

    def __str__(self):
        if self.gusts:
            return f"{self.speed} м/с (до {self.gusts} м/с) {self.direction}"
        else:
            return f"{self.speed} м/с {self.direction}"

    @staticmethod
    def direction_str(direction):
        if 22.5 < direction <= 67.5:
            return "СВ ⇙"
        elif 67.5 < direction <= 112.5:
            return "В ⇐"
        elif 112.5 < direction <= 157.5:
            return "ЮВ ⇖"
        elif 157.5 < direction <= 202.5:
            return "Ю ⇑"
        elif 202.5 < direction <= 247.5:
            return "ЮЗ ⇗"
        elif 247.5 < direction <= 292.5:
            return "З ⇒"
        elif 292.5 < direction <= 337.5:
            return "СЗ ⇘"
        else:
            return "С ⇓"

