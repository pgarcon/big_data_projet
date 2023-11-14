import requests
from weather_response import WeatherResponse
from station import Station
from station_datas import StationDatas

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


# Envoi de la requête GET avec des paramètres
response = requests.get(url, params=params)

#Creation de l'objet de réponse de l'api
weather_response = WeatherResponse()

# Envoi de la requête POST avec des données JSON
# response = requests.post(url, headers=headers, json=data)

# Vérification du statut de la réponse
if response.status_code == 200:
    # Traitement de la réponse JSON
    json_response = response.json()

     # Extraction des stations
    stations = json_response.get("stations", [])
    for station in stations:
        st = Station(station)
        weather_response.add_station(st)

    # Extraction des données horaires
    hourly_data = json_response.get("hourly", {})
    for hourly_data in hourly_data.items():
        print(hourly_data)

    
    #print(json_response)
else:
    print('Erreur lors de la requête. Code de statut :', response.status_code)
    print('Contenu de la réponse :', response.text)