resource "aws_db_subnet_group" "main" {
  name       = "ps-price-tracker-db-subnet-group"
  subnet_ids = [aws_subnet.main.id, aws_subnet.secondary.id]

  tags = {
    Name = "ps-price-tracker-db-subnet-group"
  }
}

resource "aws_security_group" "rds" {
  name        = "ps-price-tracker-rds-sg"
  description = "Allow Postgres only from the EC2 security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Postgres from EC2"
    security_groups = [aws_security_group.ec2.id]
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ps-price-tracker-rds-sg"
  }
}

resource "aws_db_instance" "main" {
  identifier             = "ps-price-tracker-db"
  engine                 = "postgres"
  engine_version         = "16"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = "ps_price_tracker"
  username               = "scraper_user"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  skip_final_snapshot    = true
  publicly_accessible    = false

  tags = {
    Name = "ps-price-tracker-db"
  }
}