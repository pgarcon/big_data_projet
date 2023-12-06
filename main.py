from pyspark.sql import SparkSession

# Define Spark session
spark = SparkSession.builder \
    .appName("MongoDBExample") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27019/test.myFirstOne") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27019/test.myFirstOne") \
    .getOrCreate()

# Now you can use the 'spark' variable in the rest of your script
df = spark.read.format("mongo").load()

# Perform operations on the DataFrame 'df'
# ...

# Finally, stop the Spark session when you're done
spark.stop()
