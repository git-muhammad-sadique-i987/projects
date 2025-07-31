<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Build a Virtual Private Cloud

**Project Link:** [View Project](http://learn.nextwork.org/projects/aws-networks-vpc)

**Author:** Muhammad Sadique  
**Email:** saddi2u@gmail.com

---

## Build a Virtual Private Cloud (VPC)

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-vpc_2facf927)

---

## Introducing Today's Project!

### What is Amazon VPC?

Amazon VPC (Virtual Private Cloud) is a service that allows you to create a logically isolated section of the AWS cloud, providing you with a virtual network to launch your AWS resources. It gives you control over your virtual networking environment, including IP address ranges, subnets, route tables, and security groups. This means you can tailor your network to your specific needs, enhancing security, flexibility, and control over your AWS infrastructure.

### How I used Amazon VPC in this project

I set up a VPC with public subnet. I attached an internet gateway to this VPC for internet connectivity.

### One thing I didn't expect in this project was...

Every thing went fine.

### This project took me...

30 minuts

---

## Virtual Private Clouds (VPCs)

VPCs are Virtual Private Cloud, a container for AWS resources like EC2 instances etc. 

There was already a default VPC in my account ever since my AWS account was created. This is because AWS wants us to have a default container in which we can put our resources like EC2 Instance. Though we can create a custom VPC as well that might suit our needs.

Start your response with 'To set up my VPC, I had to define an IPv4 CIDR block, which is a way to assign a whole block of IP addresses, kind of like creating a zone/area in a city.

To understand how big a CIDR block is, look at the number after the slash - the smaller the number, the larger the CIDR block!

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-vpc_2facf927)

---

## Subnets

Subnets are subsets of VPC spread over AZs in an AWS region. There are already subnets existing in my account, one for every AZ.

Once I created my subnet, I enabled "auto-assign public IPv4 addresses". This setting makes sure that my resource in this subnet gets a public IP so they can reach internet.

The difference between public and private subnets are:
A public subnet is connected to the internet 🌐 Resources inside a public subnet can communicate with external networks.

A private subnet does not have direct internet access 🔐 You'd use it for internal resources that don’t need to be publicly accessible.

For a subnet to be considered public, it has to an internet gateway.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-vpc_157c4219)

---

## Internet gateways

Internet gateways are key to making applications available on the internet. By attaching an internet gateway, your instances can access the internet and be accessible to external users.

Attaching an internet gateway to a VPC means connecting it to the public internet. If i missed this step, even EC2 instances with Public IPs will not be able to connect to the internet.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-vpc_4ae90410)

---

## Using the AWS CLI

---

---
