from station_datas import StationDatas

class Hourly:

    def __init__(self):
        self.data = {}

    def add_data(self, station_id, data_list):
        self.data[station_id] = [StationDatas(entry) for entry in data_list]

    def __str__(self):
        return f"Hourly(data={self.data})"
