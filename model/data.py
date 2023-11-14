import requests
from model.weather_response import WeatherResponse
from model.station import Station
from model.station_datas import StationDatas
from model.hourly import Hourly

class Data:

    def __init__(self):
        self.response = WeatherResponse()



    def sendResquest(self):
        url = 'https://www.infoclimat.fr/opendata/'

        # Si vous avez des paramètres à inclure dans la requête, vous pouvez les spécifier dans le dictionnaire params
        params = {
            'method' : 'get',
            'format' : 'json',
            'stations[]' : '000AC',
            'start' : '2023-11-12',
            'end' : '2023-11-14',
            'token' : 'd6IjJeVwkRDpv0yBBrJgIl6Kge9zAp6HubW1p1qh9QMUy1eDXnsHLw'
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
            print("#### Status OK")
            json_response = response.json()

            print("Stations extraction...")
            # Extraction des stations
            stations = json_response.get("stations", [])
            for station in stations:
                st = Station(station)
                print("Station extract : \n[\n", st, "\n]\n")
                self.response.add_station(st)

            print("Hourly extraction...")
            # Extraction des données horaires
            hourly_data = json_response.get("hourly", {})
            for id_station, hourly_data in hourly_data.items():
                for data in hourly_data:
                    #c'est l'objet param, ça nous interesse pas
                    if isinstance(data, str):
                        print(data, "is not interesting")
                    else:
                        sd = StationDatas(data)
                        hr = Hourly(st.getId(), sd)
                        print("Hourly extracted : ", hr)
                        self.response.add_hourly(hr)

            
            #print(json_response)
        else:
            print('Erreur lors de la requête. Code de statut :', response.status_code)
            print('Contenu de la réponse :', response.text)

        return self.response



    def getData(self):
        return self.response