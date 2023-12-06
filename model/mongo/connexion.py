
from pyspark.sql import SparkSession

class Mongodb:

    def __init__(self, port="27017", database=None, collection=None):
        self.spark = None
        self.port = port
        self.database = database
        self.collection = collection
        self.format = "com.mongodb.spark.sql.DefaultSource"

        self.uri = "mongodb://localhost:" + self.port + "/" + self.database + "." + self.collection
        print("### URI Mongodb : ", self.uri, " ####")
    
    
    def connexion(self):

        self.spark = SparkSession.builder \
            .appName("MongoDBExample") \
            .config("spark.mongodb.input.uri", self.uri) \
            .config("spark.mongodb.output.uri", self.uri) \
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
            .getOrCreate()
    
    def get_data(self):
        return self.spark.read.format(self.format).load().drop('_id')
    
    def add_data(self, df, data):
        # Écrire les données dans MongoDB
        df.write.format(self.format) \
            .mode("append") \
            .option("uri", self.uri) \
            .save()


    def close_connection(self):
        if self.spark == None:
            raise "Erreur, connexion non instanciée"
        else:
            self.spark.stop()