class StationDatas:

    def __init__(self, data):
        self.id_station = data.get("id_station", None)
        self.dh_utc = data.get("dh_utc", None)
        self.temperature = data.get("temperature", None)
        self.pressure = data.get("pression", None)
        self.humidity = data.get("humidite", None)
        self.dew_point = data.get("point_de_rosee", None)
        self.wind_speed = data.get("vent_moyen", None)
        self.wind_gusts = data.get("vent_rafales", None)
        self.wind_direction = data.get("vent_direction", None)
        self.rain_3h = data.get("pluie_3h", None)
        self.rain_1h = data.get("pluie_1h", None)

    def __str__(self):
        return f"StationData(id_station={self.id_station}, dh_utc={self.dh_utc}, temperature={self.temperature}, pressure={self.pressure}, humidity={self.humidity}, dew_point={self.dew_point}, wind_speed={self.wind_speed}, wind_gusts={self.wind_gusts}, wind_direction={self.wind_direction}, rain_3h={self.rain_3h}, rain_1h={self.rain_1h})"