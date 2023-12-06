from model.mongo.connexion import Mongodb as mdb

db = mdb(port="27019", database="meteo", collection="meteo")

db.connexion()

df = db.get_data()

print("\n###### Mes données : ", df, " #######\n")

db.close_connection()

