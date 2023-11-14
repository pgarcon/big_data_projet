from station import Station
from station_datas import StationDatas
from hourly import Hourly

class WeatherResponse:
    def __init__(self):
        self.stations = []
        self.hourly = []

    def add_station(self, station):
        if isinstance(station, Station):
            self.stations.append(station)
        else:
            raise ValueError("L'objet ajouté n'est pas une instance de la classe Station")

    def add_hourly(self, data, id_station):
        if isinstance(hourly, Hourly):
            self.hourly.add_data(id_station, hourly)
        else:
            raise ValueError("L'objet ajouté n'est pas une instance de la classe StationData")

    def __str__(self):
        return f"WeatherData(stations={self.stations}, station_data={self.hourly})"
