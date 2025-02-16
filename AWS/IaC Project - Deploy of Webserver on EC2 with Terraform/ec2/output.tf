output "WebServerPublicIp" {
  value = aws_instance.WebServerInstance.public_ip
}

