import json
import requests
from datetime import date, timedelta


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

    @staticmethod
    def user_str_convert(func):
        def wrapped(self, user, *args):
            user = str(user)
            return func(self, user, *args)
        return wrapped

    @user_str_convert
    def all_spots_names(self, user):
        """
        Возвращает список мест, берет ключи из словаря (имена мест)
        """
        if user in self.spots:
            return [spot for spot in self.spots[user]]
        return []

    @user_str_convert
    def spot_coord(self, user, spot):
        """
        Принимает имя места, и если оно есть в списке self.spots возвращает его координаты
        """
        if spot in self.spots[user]:
            return self.spots[user][spot]

    def data_write(self):
        with open(self.json_file, "w", encoding="utf-8") as file:
            json.dump(self.spots, file, ensure_ascii=False)

    @user_str_convert
    def add_spot(self, user, spot_name, spot_coord):
        if user not in self.spots:
            self.spots[user] = {spot_name: spot_coord}
        else:
            self.spots[user][spot_name] = spot_coord
        self.data_write()

    @user_str_convert
    def del_spot(self, user, spot_name):
        if user in self.spots:
            if spot_name in self.spots[user]:
                del self.spots[user][spot_name]
            else:
                raise ValueError
        else:
            raise ValueError


class Weather:
    def __init__(self, coord, spot_name):
        self.__coord = coord
        self.__spot_name = spot_name
        self.__cur_date = date.today()

    def weather(self):
        req = self.__request_for_api(self.__cur_date, self.__cur_date)
        answer = f"Погода {self.__spot_name}\n" \
                 f"{self.__cur_date}" \
                 f"\n\n" \
                 f"Сейчас:\n" \
                 f"Температура: {req['current_weather']['temperature']}°C\n" \
                 f"Ветер: {Wind(req['current_weather']['windspeed'], req['current_weather']['winddirection'])}" \
                 f"\n\n" \
                 f"10:00\n" \
                 f"Температура: {req['hourly']['temperature_2m'][10]}°C\n" \
                 f"Ветер: {Wind(req['hourly']['windspeed_10m'][10], req['hourly']['winddirection_10m'][10], req['hourly']['windgusts_10m'][10])}" \
                 f"\n\n" \
                 f"12:00\n" \
                 f"Температура: {req['hourly']['temperature_2m'][12]}°C\n" \
                 f"Ветер: {Wind(req['hourly']['windspeed_10m'][12], req['hourly']['winddirection_10m'][12], req['hourly']['windgusts_10m'][12])}" \
                 f"\n\n" \
                 f"14:00\n" \
                 f"Температура: {req['hourly']['temperature_2m'][14]}°C\n" \
                 f"Ветер: {Wind(req['hourly']['windspeed_10m'][14], req['hourly']['winddirection_10m'][14], req['hourly']['windgusts_10m'][14])}" \
                 f"\n\n" \
                 f"16:00\n" \
                 f"Температура: {req['hourly']['temperature_2m'][16]}°C\n" \
                 f"Ветер: {Wind(req['hourly']['windspeed_10m'][16], req['hourly']['winddirection_10m'][16], req['hourly']['windgusts_10m'][16])}"
        return answer

    def five_day_weather(self):
        """
        Функция для получения погоды на 5 дней

        Возвращает:
        str: Прогноз погоды на 5 дней
        """
        start_date = self.__cur_date + timedelta(days=1)
        req = self.__request_for_api(start_date, self.__cur_date + timedelta(days=6))
        answer = f"Погода на 5 дней {self.__spot_name}\n\n" \
                 f"{start_date}\n\n" \
                 f"{self._hour_block(1, 11, req)}\n" \
                 f"{self._hour_block(1, 15, req)}\n\n" \
                 f"{start_date + timedelta(days=1)}\n\n" \
                 f"{self._hour_block(2, 11, req)}\n" \
                 f"{self._hour_block(2, 15, req)}\n\n" \
                 f"{start_date + timedelta(days=2)}\n\n" \
                 f"{self._hour_block(3, 11, req)}\n" \
                 f"{self._hour_block(3, 15, req)}\n\n" \
                 f"{start_date + timedelta(days=3)}\n\n" \
                 f"{self._hour_block(4, 11, req)}\n" \
                 f"{self._hour_block(4, 15, req)}\n\n" \
                 f"{start_date + timedelta(days=4)}\n\n" \
                 f"{self._hour_block(5, 11, req)}\n" \
                 f"{self._hour_block(5, 15, req)}"
        return answer

    def weekend_weather(self):
        weekend = self.__weekend_days()
        req = self.__request_for_api(weekend[0], weekend[1])
        answer = f"Погода на выходные {self.__spot_name}\n\n" \
                 f"{weekend[0]}\n" \
                 f"{self._hour_block(1, 10, req)}\n" \
                 f"{self._hour_block(1, 12, req)}\n" \
                 f"{self._hour_block(1, 14, req)}\n" \
                 f"{self._hour_block(1, 16, req)}\n\n" \
                 f"{weekend[1]}\n" \
                 f"{self._hour_block(2, 10, req)}\n" \
                 f"{self._hour_block(2, 12, req)}\n" \
                 f"{self._hour_block(2, 14, req)}\n" \
                 f"{self._hour_block(2, 16, req)}\n"
        return answer

    def __weekend_days(self):
        weekday = self.__cur_date.isocalendar()
        saturday = date.fromisocalendar(weekday[0], weekday[1], 6)
        sunday = date.fromisocalendar(weekday[0], weekday[1], 7)
        return saturday, sunday

    def __request_for_api(self, start_date, stop_date):
        req = f"https://api.open-meteo.com/v1/forecast?{self.__coord}&hourly=temperature_2m,windspeed_10m," \
              f"windgusts_10m,winddirection_10m&windspeed_unit=ms" \
              f"&timezone=auto&start_date={start_date}&end_date={stop_date}" \
              f"&current_weather=true"
        answer = requests.get(req)
        answer = json.loads(answer.text)
        return answer

    def __wind_request_for_hour(self, day, hour, req):
        index = self.__get_index(day, hour)
        return Wind(req['hourly']['windspeed_10m'][index],
                    req['hourly']['winddirection_10m'][index],
                    req['hourly']['windgusts_10m'][index])

    def _hour_block(self, day, hour, req):
        return f"{hour}:00\n" \
                 f"Температура: {req['hourly']['temperature_2m'][self.__get_index(day, hour)]}°C\n" \
                 f"Ветер: {self.__wind_request_for_hour(day, hour, req)}\n" \


    @staticmethod
    def __get_index(day, hour):
        """
        Функция возвращает индекс, соответствующий указанному дню и часу.

        Аргументы:
        day (int): номер дня
        hour (int): номер часа (от 0 до 23)

        Возвращает:
        int: индекс
        """
        return (day - 1) * 24 + hour


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

