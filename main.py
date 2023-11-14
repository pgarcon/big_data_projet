from model.data import Data
from model.weather_response import WeatherResponse

donnee = Data()

reponse = donnee.sendResquest()


print("\n\n#### RESPONSE API ####\n\n")

for hourly in reponse.getAllHourly():
    print(hourly)
