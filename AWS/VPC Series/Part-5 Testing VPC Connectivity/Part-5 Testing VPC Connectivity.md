<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Testing VPC Connectivity

**Project Link:** [View Project](http://learn.nextwork.org/projects/aws-networks-connectivity)

**Author:** Muhammad Sadique  
**Email:** saddi2u@gmail.com

---

## Testing VPC Connectivity

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-connectivity_8ee57662)

---

## Introducing Today's Project!

### What is Amazon VPC?

Amazon Virtual Private Cloud (VPC) allows users to create isolated virtual networks within the Amazon Web Services (AWS) cloud, providing a secure and controlled environment for their AWS resources. It's useful because it offers enhanced security, customization, and flexibility compared to a traditional public cloud setup, allowing users to tailor their network to specific needs and security requirements.

### How I used Amazon VPC in this project

I used VPC to allow traffic between my public and private ec2 instances.

### One thing I didn't expect in this project was...

Nothing.

### This project took me...

1 hour.

---

## Connecting to an EC2 Instance

Connectivity means how well different parts of your network talk to each other and with external networks. It's essential because connectivity is how data flows smoothly across your network, powering everything from simple web hosting on the Internet to complex operations.

My first connectivity test was whether I could connect to my public ec2 instance.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-connectivity_88727bef)

---

## EC2 Instance Connect

I connected to my EC2 instance using EC2 Instance Connect, which is shortcut to log into EC2 Instance without managing SSH keys.

My first attempt at getting direct access to my public server resulted in an error, because the security group attached to ec2 instance was blocking the SSH Port-22.

I fixed this error by allowing traffic into SSH port 22 inbound.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-connectivity_1cbb1b88)

---

## Connectivity Between Servers

Ping is a computer network tool used to test the reachability of a host and measure the round-trip time (latency) of network requests. It works by sending an "echo request" to a target device and measuring the time it takes to receive an "echo reply". 

The ping command I ran was ping 10.0.1.206

The first ping returned nothing. This meant that the ping could not reached back to source EC2.


![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-connectivity_defghijk)

---

## Troubleshooting Connectivity

I troubleshooted this by allowing ICMP traffic both on Private NACL and Private security group.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-connectivity_4a9e8014)

---

## Connectivity to the Internet

cURL is a command-line tool and library used for transferring data with URLs. It supports a wide range of protocols, including HTTP, HTTPS, FTP, and more. Essentially, it allows you to interact with servers, making requests and receiving responses, which is useful for tasks like downloading files, sending data, and interacting with APIs

I used curl to test the connectivity between my public ec2 instance and internet.

### Ping vs Curl

Ping: To test if a server is reachable and measure latency. cURL: To fetch data from a URL or test an API.

---

## Connectivity to the Internet

I ran the curl command 'curl https://learn.nextwork.org/projects/aws-host-a-website-on-s3' which returned HTML contents of that webpage.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-connectivity_8ee57662)

---

---
