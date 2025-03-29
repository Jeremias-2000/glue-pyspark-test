from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("GlueJob") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://172.19.0.2:4566") \
    .config("spark.hadoop.fs.s3a.access.key", "AKIAP089D0A1B3AE5BFE") \
    .config("spark.hadoop.fs.s3a.secret.key", "12345678") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()


s3_url = "s3a://glue-bucket-example"

df = spark.read.option("header", "true").csv(f"{s3_url}/MOCK_DATA.csv")


print('mostrar dados carregados do csv')
df.show()


print('mostrar os dados filtrados')

df_filtrado = df.filter(df["country_code"] == "BR")

df.show()

df_filtrado.write.mode('overwrite').parquet(f"{s3_url}/parquet/filtered_data.parquet")