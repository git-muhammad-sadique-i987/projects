resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.lab_vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "Private-Subnet"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                = aws_vpc.lab_vpc.id
  cidr_block            = "10.0.2.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "Public-Subnet"
  }
}
