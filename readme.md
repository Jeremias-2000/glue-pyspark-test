# AWS Glue Local Test with LocalStack and PySpark

<img src="aws-glue.svg" alt="AWS Glue" width="50"/> <img src="s3.svg" alt="S3" width="50"/> <img src="localstack.jpg" alt="LocalStack" width="50"/> <img src="pyspark.png" alt="PySpark" width="50"/>

This guide demonstrates how to test AWS Glue locally using Docker, LocalStack, and PySpark. You'll learn how to set up AWS CLI, interact with S3 buckets in LocalStack, and run a PySpark job for querying and transforming data.

## Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [LocalStack](https://localstack.cloud/)
- [AWS CLI](https://aws.amazon.com/cli/) (configured for LocalStack)
- [PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Terraform](https://developer.hashicorp.com/terraform/downloads) (optional, for infrastructure as code)

## Steps

### 1. Start LocalStack with Docker Compose

First, authenticate Docker with AWS ECR (for the public AWS Glue image):

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

Then, start LocalStack:

```bash
docker-compose up --build
```

### 2. Configure AWS CLI for LocalStack

Run the following command to configure AWS CLI to use LocalStack:

```bash
awslocal configure
```

If you're using Terraform, adjust your `terraform.tfvars` file accordingly.

### 3. Create an S3 Bucket and Upload CSV File

Create a test S3 bucket in LocalStack:

```bash
awslocal s3 mb s3://glue-bucket-example
```

Upload a CSV file to LocalStack's S3 bucket:

```bash
awslocal s3 cp /path/to/LOCAL_CSV_FILE.csv s3://glue-bucket-example/MOCK_DATA.csv
```

### 4. Verify Buckets and Objects in S3

List all available S3 buckets:

```bash
awslocal s3api list-buckets
```

List objects in the `glue-bucket-example` bucket:

```bash
awslocal s3api list-objects --bucket glue-bucket-example
```

### 5. Run PySpark with AWS Glue Configuration

Launch a PySpark session with LocalStack S3 integration:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("GlueJob") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:4566") \
    .config("spark.hadoop.fs.s3a.access.key", "test") \
    .config("spark.hadoop.fs.s3a.secret.key", "test") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

s3_url = "s3a://glue-bucket-example"
df = spark.read.option("header", "true").csv(f"{s3_url}/MOCK_DATA.csv")
df.show()

df_filtered = df.filter(df["country_code"] == "BR")
df_filtered.show()

df_filtered.write.mode("overwrite").parquet(f"{s3_url}/parquet/filtered_data.parquet")
```

### 6. Run the PySpark Script in Docker

To run the script inside the LocalStack container, first copy your script into the container:

```bash
docker cp /path/to/script.py <container_id>:/home/hadoop/script.py
```

Access the container:

```bash
docker exec -it --user root <container_id> bash
```

Move the script to the correct directory and run PySpark:

```bash
mv /tmp/script.py /home/hadoop/
pyspark --conf spark.sql.catalogImplementation=hive
```

---

## Notes

- Replace `/path/to/LOCAL_CSV_FILE.csv` and `/path/to/script.py` with actual file paths.
- Replace `<container_id>` with the ID of your LocalStack container (`docker ps` helps find it).
- LocalStack may introduce some latency when accessing S3. If you encounter `AccessDeniedException`, wait a few seconds and retry.
- If using Terraform, ensure that S3 and IAM configurations are correctly defined.

---

This guide helps you test AWS Glue locally with LocalStack and PySpark, enabling data processing without an actual AWS account. 🚀

