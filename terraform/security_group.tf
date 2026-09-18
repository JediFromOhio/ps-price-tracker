resource "aws_security_group" "ec2" {
  name        = "ps-price-tracker_sg"
  description = "Security group for ps-price-tracker"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.my_ip}/32"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "ps-price-tracker_sg"
    Project = "ps-price-tracker"
  }

}