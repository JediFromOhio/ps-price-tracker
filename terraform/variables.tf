variable "my_ip" {
  description = "My public IP address, for SSH access"
  type        = string
}

variable "db_password" {
  description = "Password for the RDS database"
  type        = string
  sensitive   = true
}