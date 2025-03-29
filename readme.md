# AWS Glue Local Test with LocalStack and PySpark

This guide demonstrates how to test AWS Glue locally using Docker, LocalStack, and PySpark. It includes steps to configure AWS CLI, interact with S3 buckets in LocalStack, and run a PySpark job for querying data.

## Prerequisites

1. Docker
2. LocalStack
3. AWS CLI (configured with LocalStack)
4. Terraform (optional, if using configuration variables)
5. PySpark

## Steps

### 1. Set up Docker and LocalStack

First, use the following command to authenticate Docker with AWS ECR (for the public AWS Glue image):

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

Then, start LocalStack with Docker Compose:

```bash
docker-compose up --build
```

### 2. Configure AWS CLI with LocalStack

Run the following command to configure AWS CLI to use LocalStack:

```bash
awslocal configure
```

You may also want to adjust your `terraform.tfvars` file for Terraform configuration if needed.

### 3. Add CSV File to LocalStack S3

To add a CSV file to LocalStack's S3 bucket, use the following command to copy the file into the LocalStack container:

```bash
docker cp /path/to/your/LOCAL_CSV_FILE.csv <container_id>:/opt/code/localstack/LOCAL_CSV_FILE.csv
```

Then, upload the file to your LocalStack S3 bucket using:

```bash
awslocal --endpoint-url=http://localhost:4566 s3 cp /opt/code/localstack/LOCAL_CSV_FILE.csv s3://glue-bucket-example/LOCAL_CSV_FILE.csv
```

### 4. List Buckets and Objects in S3

To list all the S3 buckets:

```bash
awslocal s3api list-buckets
```

To list objects in a specific bucket:

```bash
awslocal s3api list-objects --bucket glue-bucket-example
```

### 5. Copy Script to Container and Run PySpark

To run PySpark in the LocalStack container, copy your script file into the container:

```bash
docker cp /path/to/your/script.py <container_id>:/home/hadoop/script.py
```

Then, enter the container and move the script to the correct directory:

```bash
docker exec -it --user root <container_id> bash
mv /tmp/script.py /home/hadoop/
```

Finally, you can run PySpark with the following command:

```bash
pyspark --conf spark.sql.catalogImplementation=hive
```

This will start your PySpark session and you can execute your queries.

---

### Notes

- Replace `/path/to/your/LOCAL_CSV_FILE.csv` and `/path/to/your/script.py` with the actual paths to your CSV and Python script files.
- `<container_id>` should be replaced with the ID of your running LocalStack container.
- You can configure the bucket names and other settings based on your project requirements.

---

This README summarizes the steps to test AWS Glue locally with LocalStack and PySpark, ensuring you can query data from S3 using PySpark without needing an actual AWS account.

