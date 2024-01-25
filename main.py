from model.mongo.mongodb import Mongodb as mdb
from model.data import Data
from model.IA.model import Prediction
import pandas as pd

db = mdb(port="27019", database="meteo", collection="meteo")
db.connexion()
df = db.get30jours()

pred = Prediction()
pred.prepare_data()
#pred.train_model()

pred.train_model()



pred.predict(data=df)



#df = db.request(date_deb='2024-01-08', date_fin='2024-01-09', token="VjEA2gemNUZnzvTXyLNZB4QOpTgeNdPgazDbh6tlE8KuWl3YqBxvg")

#db.get_data()
#db.requestOneYears(years="2022", token="LEx7auQCHnZ70jWWLTNkZD0lRzzg9Lq89vfkrwu9qCT2g4rpN0hQg")
#df = db.request(date_deb="2024-01-17", date_f="2024-01-18", token="LEx7auQCHnZ70jWWLTNkZD0lRzzg9Lq89vfkrwu9qCT2g4rpN0hQg")

#db.close_connection()

#print("\nPrédiction : ", pred.predict(df))


