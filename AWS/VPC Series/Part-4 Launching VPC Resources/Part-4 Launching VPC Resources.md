<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Launching VPC Resources

**Project Link:** [View Project](http://learn.nextwork.org/projects/aws-networks-ec2)

**Author:** Muhammad Sadique  
**Email:** saddi2u@gmail.com

---

## Launching VPC Resources

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-ec2_8ee57662)

---

## Introducing Today's Project!

### What is Amazon VPC?

Amazon VPC (Virtual Private Cloud) is a service that allows you to create a logically isolated section within the AWS Cloud, essentially a virtual network where you can launch AWS resources. It's useful because it gives you fine-grained control over your network configuration, enabling you to enhance security and manage your cloud resources more effectively. 


### How I used Amazon VPC in this project

I explored "VPC and more" option today, which offers an automated way of creating multiple VPC resources at once i.e. Subnets, Route Tables, Internet Gateways, VPC Endpoint and NAT Gateways.

### One thing I didn't expect in this project was...

Every thing went fine

### This project took me...

60 Minuts.

---

## Setting Up Direct VM Access

Directly accessing a virtual machine means logging into and managing the operating system or software of the machine as if you were using it in front of you, but over the internet.

The AWS Management Console gives you a user-friendly interface to set up and manage AWS resources, but it doesn't typically provide direct access to the operating systems of your EC2 instances. For operations that require direct OS-level access, like installing software, editing configuration files, or running scripts, you'd use your key pair to connect directly. This method of access is essential for deeper administrative tasks or specific kinds of troubleshooting that can't be performed through the console.

### SSH is a key method for directly accessing a VM

SSH, or Secure Shell, is the protocol we use for this secure access to a remote machine. When you connect to the instance, SSH verifies you possess the correct private key corresponding to the public key on the server, ensuring only authorized users can access the instance.

### To enable direct access, I set up key pairs

In Amazon Web Services (AWS), a key pair is a secure way to control access to your EC2 instances. It consists of a public key and a private key, used together for secure communication. When you launch an EC2 instance, you specify a key pair. The public key is stored on the instance, while the private key is downloaded to your computer. You use the private key to securely connect to the instance, typically via SSH (for Linux) or RDP (for Windows).

Just like how documents can be saved in various file formats like PDF, DOCX, or TXT, each suited for different applications or systems, private keys also come in different file formats. Not every system or application can process all these formats, so choosing the right one is crucial.

The .pem format, which stands for Privacy Enhanced Mail, started off as a way to secure emails but has since become the go-to format for managing cryptographic keys because it is supported by many different types of servers e.g. EC2 instances!

---

## Launching a public server

I had to change my EC2 instance's networking settings by choosing existing subnet i.e. Next Work public subnet.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-ec2_88727bef)

---

## Launching a private server

My private server has its own dedicated security group because it does not require public access. So i created a more restrictive security group which only allow ssh connection from existing "NextWork Public Security Group".

My private server's security group's source is "NextWork Public Security Group" which only allow ssh connection from resources into that security group. This reduced the attack surface of my private Ec2 instance.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-ec2_4a9e8014)

---

## Speeding up VPC creation

I used an alternative way to set up an Amazon VPC! This time, I chose "VPC and more" option while creating VPC, which offers a streamlined and automated way to set up a basic, yet functional, Virtual Private Cloud (VPC) environment. This option is designed to simplify the initial configuration by automatically provisioning several essential components (e.g Subnets, Route Tables & IGW) required for a standard cloud deployment.


A VPC resource map is a visual representation of the resources within an Amazon Virtual Private Cloud (VPC) and their connections, helping users understand the architecture and relationships of their cloud network.

My new VPC has a CIDR block of 10.0.0.0/16. It is possible for my new VPC to have the same IPv4 CIDR block as my existing VPC because, AWS VPCs are isolated from each other by default, so there won't be any IP conflicts unless you explicitly connect them using VPC peering.
However, this set up will mean your overlapping VPCs can't talk to each other directly. That's why it'd be best practice to have completely unique CIDR blocks for each VPC in your account!

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-ec2_1cbb1b88)

---

## Speeding up VPC creation

### Tips for using the VPC resource map

When determining the number of public subnets in my VPC, I only had two options - 0 and 2. I could not create one Public subnet.

This is AWS' best practice advice at work! When you pick 2 Availability Zones, the wizard makes sure you have a public subnet in each one. This way, your public resources stay up even if one of the two Availaiblity Zones goes down.

The set up page also offered to create NAT gateways, which are cloud services that allow instances within a private subnet to connect to the internet or other cloud services while keeping those instances inaccessible to unsolicited inbound connections from the internet

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-ec2_8ee57662)

---

---
