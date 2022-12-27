import json
import requests


class Spots:
    def __init__(self, json_file):
        self.json_file = json_file
        with open(self.json_file, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
        self.spots = data

    def all_spots_names(self):
        return [spot for spot in self.spots]

    def spot_coord(self, spot):
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


