#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo service httpd start

# Fetch instance metadata
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/region)
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Create index.html with desired message
echo "<h1>Hello World from ${PUBLIC_IP} and ${REGION}</h1>" | sudo tee /var/www/html/index.html

sudo systemctl enable httpd
