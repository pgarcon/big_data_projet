from model.data import Data
import pandas as pd
from model.weather_response import WeatherResponse

donnee = Data(token='CHDuxKEEdnwFpY3RbJPZAWdTNoLBKK7Q3tg90D0lukS0dgBAh1Qw')

reponse = donnee.requestAllStations()

print(reponse)

