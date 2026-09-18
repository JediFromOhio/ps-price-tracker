terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0"
        }
    }
}


# Configure the AWS Provider
provider "aws" {
    region = "us-east-1"
    profile = "ps-price-tracker"
}


# Create an S3 bucket to store Terraform state
resource "aws_s3_bucket" "terraform_state" {
    bucket = "ps-price-tracker-tfstate"

    lifecycle {
        prevent_destroy = true
    }
}


resource "aws_s3_bucket_versioning" "terraform_state" {
    bucket = aws_s3_bucket.terraform_state.id

    versioning_configuration {
        status = "Enabled"
    }
}


