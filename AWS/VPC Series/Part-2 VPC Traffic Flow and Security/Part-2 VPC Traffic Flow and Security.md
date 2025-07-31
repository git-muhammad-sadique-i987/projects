<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# VPC Traffic Flow and Security

**Project Link:** [View Project](http://learn.nextwork.org/projects/aws-networks-security)

**Author:** Muhammad Sadique  
**Email:** saddi2u@gmail.com

---

## VPC Traffic Flow and Security

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-security_92b0b0b4)

---

## Introducing Today's Project!

### What is Amazon VPC?

Amazon VPC (Virtual Private Cloud) is a service that allows you to create a logically isolated section of the AWS Cloud where you can launch AWS resources, such as EC2 instances, in a virtual network that you define.

### How I used Amazon VPC in this project

I used Amazon VPC in todays project to create multiple resource inside it e.g. Subnets, NACLs, Sercurity Groups etc. I created IGW and attach it my VPC.

### One thing I didn't expect in this project was...

Nothing.

### This project took me...

60 Minuts.

---

## Route tables

Route tables are like GPS maps which directs traffic to its destination by sending it to the target aka next-hop in more network centric language. A default route toward IGW will forward all the traffic towards internet. However, traffic that is destined to internal network of VPC i.e. 10.0.0.0/16 will be not leave VPC.

A subnet is not considered Public unless its traffic is directed toward Internet Gateway. Route doe the job of directing a subnet traffic to the target or next-hop, in this case Internet gateway.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-security_0a07b191)

---

## Route destination and target

Destination mean the CIDR block of the traffic that we want to direct toward the target. The target is the next-hop. It could be an internet gateway or a NAT gateway as well.

Destination is 0.0.0.0/0 i.e. All IPv4 Traffic
Target Internet Gateway that we just created.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-security_0a07b191)

---

## Security groups

Security group are like stateful firewall that allows the inbound or outbound traffic toward any AWS resource that it is attached to.

### Inbound vs Outbound rules

Inbound rule means the security group rule that deals with inbound traffic toward the AWS resource that the security group is attached to. I configured an inbound rule that allows HTTP traffic inbound.

Outbound rules are for outbound traffic. By default all outbound traffic is allowed.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-security_92b0b0b4)

---

## Network ACLs

NACLs (Network Access Control Lists) are optional stateless firewalls that act as a security layer for your VPC subnets. They control traffic in and out of subnets, providing a second line of defense in addition to Security Groups, which operate at the instance level. 

### Security groups vs. network ACLs

Security groups act as a virtual firewall for instances, controlling inbound and outbound traffic at the instance level. Network ACLs, on the other hand, are stateless firewalls that operate at the subnet level, controlling traffic entering and leaving the subnet.

---

## Default vs Custom Network ACLs

### Similar to security groups, network ACLs use inbound and outbound rules

The default rules for both inbound and outbound traffic in a network ACL are configured to deny all traffic. This means that if a packet doesn't match any of the explicitly defined rules, it will be dropped.

A custom network access control list (ACL) in a VPC allows or denies specific inbound and outbound traffic at the subnet level.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-security_4faeb056)

---

## Tracking VPC Resources

I created additional VPC, IGW and SG in us-east-1 region using AWS CLI. Teams would use multiple regions to avoid SPOF and allows users in the specific region to quickly access their AWS Cloud resources.

EC2 Global View provides a centralized dashboard to view your Amazon EC2 and VPC resources across all AWS regions. It allows you to see a summary of your resources, including instances, VPCs, subnets, security groups, and volumes, as well as resource counts per region. It also offers a global search functionality to find specific resources across regions. 

EC2 Global View is used to get a unified, global view of your AWS resources, particularly EC2 instances, VPCs, subnets, security groups, and volumes, across all AWS regions. You would use it when you need to monitor or manage your resources across multiple regions in a single interface, instead of navigating to each region individually.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-security_b03ea6162)

---

---
