output "s3_bucket_url" {
  value = "http://localhost:4566/${aws_s3_bucket.example.bucket}"
}