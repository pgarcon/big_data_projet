from model.station import Station
from model.station_datas import StationDatas
from model.hourly import Hourly

class WeatherResponse:
    def __init__(self):
        self.stations = []
        self.hourly = None

    def add_station(self, station):
        if isinstance(station, Station):
            self.stations.append(station)
        else:
            raise ValueError("L'objet ajouté n'est pas une instance de la classe Station")

    def add_hourly(self, hourly):
        if isinstance(hourly, Hourly):
            self.hourly = hourly
        else:
            raise ValueError("L'objet ajouté n'est pas une instance de la classe StationData")

    def __str__(self):
        return f"WeatherData(stations={self.stations}, station_data={self.hourly})"
    

    def getHourly(self):
        return self.hourly
    
