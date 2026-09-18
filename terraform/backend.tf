terraform {
  backend "s3" {
    bucket       = "ps-price-tracker-tfstate"
    key          = "main/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    profile      = "ps-price-tracker"
    encrypt      = true
  }
}