import requests
import pandas as pd
import json
from model.weather_response import WeatherResponse
from model.station import Station
from model.station_datas import StationDatas
from model.hourly import Hourly

class Data:

    def __init__(self, token):
        self.response = WeatherResponse()
        self.token = token



    def sendResquest(self, tableau_id):
        url = 'https://www.infoclimat.fr/opendata/'

        # Si vous avez des paramètres à inclure dans la requête, vous pouvez les spécifier dans le dictionnaire params
        params = {
            'method' : 'get',
            'format' : 'json',
            'stations[]' : tableau_id,
            'start' : '2023-11-12',
            'end' : '2023-11-14',
            'token' : self.token
        }

        print("Request to : ", url)
        # Envoi de la requête GET avec des paramètres
        response = requests.get(url, params=params)
        print("Request end ")

        #Creation de l'objet de réponse de l'api
        weather_response = WeatherResponse()

        # Envoi de la requête POST avec des données JSON
        # response = requests.post(url, headers=headers, json=data)

        # Vérification du statut de la réponse
        if response.status_code == 200:
            # Traitement de la réponse JSON

            #print("#### message : ", print(response.text), " #### \n")
            print("#### Status OK")
            json_response = response.json()

            print("Stations extraction...")
            # Extraction des stations
            stations = json_response.get("stations", [])
            for station in stations:
                st = Station(station)
                #print("Station extract : \n[\n", st, "\n]\n")
                self.response.add_station(st)

            print("Hourly extraction...")
            # Extraction des données horaires
            hourly_data = json_response.get("hourly", {})
            hr = Hourly()
            for id_station, hourly_data in hourly_data.items():
                #print("\n", hourly_data)
                hr.add_data(id_station, hourly_data)
            self.response.add_hourly(hr)

        else:
            print('Erreur lors de la requête. Code de statut :', response.status_code)
            print('Contenu de la réponse :', response.text)

        liste_data = []

        for id in self.response.getHourly().getData():
            for i in range(self.response.getHourly().getSizeOf(id)):
                #print(reponse.getHourly().getStationsData(id, i))
                liste_data.append(self.response.getHourly().getStationsData(id, i))


        #print(liste_data)


        data = {
            'id_station': [station.id_station for station in liste_data],
            'dh_utc': [station.dh_utc for station in liste_data],
            'temperature': [station.temperature for station in liste_data],
            'pressure': [station.pressure for station in liste_data],
            'humidity': [station.humidity for station in liste_data],
            'dew_point': [station.dew_point for station in liste_data],
            'wind_speed': [station.wind_speed for station in liste_data],
            'wind_gusts': [station.wind_gusts for station in liste_data],
            'wind_direction': [station.wind_direction for station in liste_data],
            'rain_3h': [station.rain_3h for station in liste_data],
            'rain_1h': [station.rain_1h for station in liste_data],
        }

        df = pd.DataFrame(data)

        return df


    def requestAllStations(self):
        url = "https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson"

        print("Request to : ", url)
        response = requests.get(url)
        print("Request end to ", url)

        if response.status_code == 200:
            # Traitement de la réponse JSON
            print("#### Status OK")
            json_response = response.json()

            #print(json_response)

            tab_request = []
            feature =  json_response.get("features", [])
            for station in feature:
                if(station.get("properties").get("country") == "FR"):
                    #print(station.get("id"))
                    tab_request.append(station.get("properties").get("id"))

            return self.sendResquest(tab_request)

    def getData(self):
        return self.response