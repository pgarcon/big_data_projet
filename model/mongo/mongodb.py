
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, date_format, to_date, when
from datetime import datetime, timedelta
from model.data import Data
from pymongo import MongoClient


#table = meteo
#collection = meteo
class Mongodb:

    def __init__(self, port="27017", database=None, collection=None):
        self.spark = None
        self.port = port
        self.database = database
        self.collection = collection
        self.format = "com.mongodb.spark.sql.DefaultSource"

        self.uri = "mongodb://localhost:" + self.port + "/" + self.database + "." + self.collection
        print("### URI Mongodb : ", self.uri, " ####")
        self.client = MongoClient(self.uri)
        self.db = self.client[self.database]
        self.mongo_collection = self.db[self.collection]
    
    
    def connexion(self):

        self.spark = SparkSession.builder \
            .appName("MongoDBExample") \
            .config("spark.mongodb.input.uri", self.uri) \
            .config("spark.mongodb.output.uri", self.uri) \
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
            .getOrCreate()
    
    def get_data(self):
        df = self.spark.read.format(self.format).load().drop('_id')
        df.show()
        return df
    

    def get30jours(self):
        df = self.spark.read.format(self.format).load().drop('_id').toPandas().sort_values(by='dh_utc', ascending=False)
        df = df[:30]
        print("\n##### 30 jours ###### \n\n ", df)

        return df

    def prepare_data(self):
        sdf = self.get_data()

        #sdf = sdf.withColumn('raining', when((col('avg_rain_1h') + col('avg_rain_3h')) > 0.5, True).otherwise(False))

        return sdf.toPandas()


    
    def add_data(self, df):
        # Écrire les données dans MongoDB
        df_spark = self.spark.createDataFrame(df)

        df_spark = df_spark.na.fill(0)

        df_spark = df_spark.withColumn("dh_utc", date_format(to_date(col("dh_utc"), 'yyyy-MM-dd HH:mm:ss'), 'yyyy-MM-dd'))

        result_df = df_spark.groupBy('dh_utc').agg(
            F.avg('temperature').alias('avg_temperature'),
            F.avg('humidity').alias('avg_humidity'),
            F.avg('pressure').alias('avg_pressure'),
            F.avg('rain_1h').alias('avg_rain_1h'),
            F.avg('rain_3h').alias('avg_rain_3h'),
            F.avg('wind_speed').alias('avg_wind_speed'),
            F.avg('wind_direction').alias('avg_wind_direction'),
            F.avg('wind_gusts').alias('avg_wind_gusts')
        )

        result_df.show()
        
        result_df.write.format(self.format) \
            .mode("append") \
            .option("uri", self.uri) \
            .option("partitioner", "MongoSinglePartitioner") \
            .option("partitionKey", "id_station") \
            .save()
        
    #NE PAS UTILISER SI REQUESTONEYEARS FAITE    
    def delete_all_data(self):
        # Supprimer toutes les données de la collection
        print("Suppresion refusée")
        #result = self.mongo_collection.delete_many({})
        #print(f"{result.deleted_count} documents ont été supprimés.")

    def requestOneYears(self, years=2023, token=None):

        str_date_debut = years+'-01-01'
        print("date debut requete ! ", str_date_debut)

        date_debut = datetime.strptime(str_date_debut, '%Y-%m-%d')
        date_fin = date_debut + timedelta(days=2)  # Initialisation de la date de fin

        # Boucle pour requêter sur un an par tranches de 2 jours
        while date_fin <= datetime.strptime('2023-12-31', '%Y-%m-%d'):
            str_date_debut = date_debut.strftime('%Y-%m-%d')
            str_date_fin = date_fin.strftime('%Y-%m-%d')

            print("\n### Requete entre : ", str_date_debut, ' ET ', str_date_fin, ' ###\n')
            data = Data(token=token, date_debut=str_date_debut, date_fin=str_date_fin)
            response = data.requestAllStations()
            
            # Ajoutez ici le traitement que vous souhaitez effectuer avec les données, par exemple :
            # result = process_data(data)
            # print(result)
            self.add_data(response)

            # Incrémente les dates de 2 jours pour la prochaine requête
            date_debut += timedelta(days=2)
            date_fin = date_debut + timedelta(days=2)


    def request(self, date_deb=None, date_f=None, token=None):
        data = Data(token=token, date_debut=date_deb, date_fin=date_f)
        response = data.requestAllStations()

        self.add_data(response)

        df_spark = self.spark.createDataFrame(response)

        df_spark = df_spark.na.fill(0)

        df_spark = df_spark.withColumn("dh_utc", date_format(to_date(col("dh_utc"), 'yyyy-MM-dd HH:mm:ss'), 'yyyy-MM-dd'))

        result_df = df_spark.groupBy('dh_utc').agg(
            F.avg('temperature').alias('avg_temperature'),
            F.avg('humidity').alias('avg_humidity'),
            F.avg('pressure').alias('avg_pressure'),
            F.avg('rain_1h').alias('avg_rain_1h'),
            F.avg('rain_3h').alias('avg_rain_3h'),
            F.avg('wind_speed').alias('avg_wind_speed'),
            F.avg('wind_direction').alias('avg_wind_direction'),
            F.avg('wind_gusts').alias('avg_wind_gusts')
        )

        

        return result_df.toPandas()



    def close_connection(self):
        if self.spark == None:
            raise "Erreur, connexion non instanciée"
        else:
            self.spark.stop()