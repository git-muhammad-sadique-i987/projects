resource "aws_route_table" "lab_rt" {
  vpc_id = aws_vpc.lab_vpc.id

  tags = {
    Name = "Lab-RouteTable"
  }
}

resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.lab_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.lab_igw.id
}

resource "aws_route_table_association" "public_subnet_associate_with_rt" {
  route_table_id = aws_route_table.lab_rt.id
  subnet_id      = aws_subnet.public_subnet.id
}

resource "aws_route_table_association" "private_subnet" {
  route_table_id = aws_route_table.lab_rt.id
  subnet_id      = aws_subnet.private_subnet.id
}
