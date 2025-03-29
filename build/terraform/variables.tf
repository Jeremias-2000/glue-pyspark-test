variable "aws_access_key" {
  type        = string
  description = "AWS Access Key"
}

variable "aws_secret_key" {
  type        = string
  description = "AWS Secret Access Key"
}

variable "s3_bucket_name" {
  type        = string
  description = "The name of the S3 bucket"
}

variable "s3_bucket_url" {
  type        = string
  description = "The URL of the S3 bucket"
}