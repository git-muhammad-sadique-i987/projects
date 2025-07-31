<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Creating a Private Subnet

**Project Link:** [View Project](http://learn.nextwork.org/projects/aws-networks-private)

**Author:** Muhammad Sadique  
**Email:** saddi2u@gmail.com

---

## Creating a Private Subnet

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-private_afe1fdbd)

---

## Introducing Today's Project!

### What is Amazon VPC?

Amazon VPC (Virtual Private Cloud) is a service that allows users to create a logically isolated section within the AWS Cloud to launch AWS resources. It provides a virtual network that mimics a traditional data center network, giving users control over their networking environment, including IP address ranges, subnets, routing tables, and security. Essentially, it's a way to create a private, secure space within the AWS cloud for your applications and data.

### How I used Amazon VPC in this project

I setup a private subnet inside my VPC. Then i created a dedicated route table and a NACL for that subnet inside that VPC.

### One thing I didn't expect in this project was...

Nothing, every thing went fine.

### This project took me...

1 hour.

---

## Private vs Public Subnets

Public subnet traffic is routed to IGW whereas Private subnet traffic stays in VPC only. Private subnet traffic is not forwarded to Internet gateway (IGW).

Private subnets are useful for private resources inside a cloud-based IT Appl or setup. These resources might include DataBase or any other server that doe not require public access.

My private and public subnets cannot have the same subnets as it would cause an overlap. The routing table will not be able to decided which traffic to forward which target.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-private_afe1fdbd)

---

## A dedicated route table

By default, my private subnet is associated with default route table i.e. Public Route Table.

I had to set up a new route table because the old route table has a default route 0.0.0.0/0 towards internet gateway. If leave my private subnet to default route table, its traffice will be redirected towards internet gateway - Hence my Private subnet will no longer remain private.

My private subnet's dedicated route table only has one inbound and one outbound rule that allows internal VPC traffic.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-private_b4b904b5)

---

## A new network ACL

By default, my private subnet is associated with default NACL. 

I set up a dedicated network ACL for my private subnet because, removing a route to the internet gateway does prevent direct internet access to and from the subnet. However, relying only on route table configurations might not be great for security.

If any part of your VPC (e.g. your public subnet) gets compromised, the attacker could take advantage of your permissive ACL setup to access or attack the resources in your private subnet!

Hence a dedicated NACL for my private subnet is necessary. 

My new network ACL has two simple rules - deny all inbound and deny all outbound. I will allow the traffic only when it is required.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-private_1ed2cb07)

---

---
