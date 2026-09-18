resource "aws_key_pair" "ec2" {
  key_name   = "ps-price-tracker-key"
  public_key = file("${path.module}/ps-price-tracker.pub")
}