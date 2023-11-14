from model.data import Data
from model.weather_response import WeatherResponse

donnee = Data(token='d6IjJeVwkRDpv0yBBrJgIl6Kge9zAp6HubW1p1qh9QMUy1eDXnsHLw')

reponse = donnee.sendResquest()


print("\n\n#### RESPONSE API ####\n\n")

##OK
for hourly in reponse.getAllHourly():
    print(hourly)
