from confluent_kafka import Producer
from model.utils import PROPERTIES_FILE
from model.data import Data
import pandas as pd
from model.utils import read_ccloud_config

class ProducerClass:
    
    def produce(self):

        print("### Start producer.")
        donnee = Data(token="AoPwTySlsJxKUSdz0Rw6v0Soc5wZGtgFS8b6W9KJG8U2DCy494g")
        reponse = donnee.requestAllStations()

        producer = Producer(read_ccloud_config(PROPERTIES_FILE))

        print("Writing data")

        for i, data in reponse.iterrows():
            #print("Donnes : ", data)
            producer.produce("big_data_meteo_topic", key="1", value=data.to_json())
            producer.flush()


