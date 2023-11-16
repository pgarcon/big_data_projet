from model.station_datas import StationDatas

class Hourly:

    def __init__(self):
        self.data = {}

    def add_data(self, id_station, data_list):
        if(id_station != "_params"):
            self.data[id_station] = [StationDatas(entry) for entry in data_list if not isinstance(entry, str)]

    def __str__(self):
        return f"Hourly(data={self.data.keys})"
    

    def getStationsData(self, id_station, index):
        return self.data[id_station][index]
    
    def getSizeOf(self, id_station):
        return len(self.data[id_station])
    
    def getData(self):
        return self.data
