resource "aws_instance" "WebServerInstance" {
  ami                    = data.aws_ami.latest_amazon_linux.id
  instance_type          = "t2.micro"
  key_name               = "Siddique_Key"
  vpc_security_group_ids = [aws_security_group.lab_sg.id]
  subnet_id              = aws_subnet.public_subnet.id

  user_data = file("setup.sh")

  tags = {
    Name = "Web-Server"
  }
}
