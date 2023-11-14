from model.station_datas import StationDatas

class Hourly:

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def add_data(self, data_list):
        self.data[self.name] = [StationDatas(entry) for entry in data_list]

    def __str__(self):
        return f"Hourly(data={self.data})"
