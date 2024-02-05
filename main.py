from model.mongo.mongodb import Mongodb as mdb
from model.data import Data
from model.IA.model import Prediction
import pandas as pd

db = mdb(port="27019", database="meteo", collection="meteo")
db.connexion()
#df = db.get30jours()
#df2 = db.getDataPerMonth()

db.getDataPerMonth(2023)

#pred = Prediction()
#pred.prepare_data()
#pred.train_model()

#pred.chargeModel()
#pred.evaluate()

#pred.train_model()



#pred.predict(data=df)


#db.request(date_deb='2024-01-26', date_f='2024-01-27', token="94m12xFXgjJdImxKoAV20XtnFCzXTG3ZMmmTZFRv8Lmm7CUG6NQ")
#db.request(date_deb='2024-01-28', date_f='2024-01-29', token="94m12xFXgjJdImxKoAV20XtnFCzXTG3ZMmmTZFRv8Lmm7CUG6NQ")
#db.request(date_deb='2024-01-31', date_f='2024-01-31', token="3gWx5y56sHi4IK0KBtaHIbb0omMiynyhpkQBPK0yRljozZdiCfb2A")

#db.get_data()
#db.requestOneYears(years="2020", token="Ned554izTiCL75hhUCP9bxjZWAxC3DsPRrGphhNqH1AkdsyS5bvbQ")
#df = db.request(date_deb="2024-01-17", date_f="2024-01-18", token="LEx7auQCHnZ70jWWLTNkZD0lRzzg9Lq89vfkrwu9qCT2g4rpN0hQg")

#db.close_connection()

#print("\nPrédiction : ", pred.predict(df))


