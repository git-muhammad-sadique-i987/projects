<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# VPC Monitoring with Flow Logs

**Project Link:** [View Project](http://learn.nextwork.org/projects/aws-networks-monitoring)

**Author:** Muhammad Sadique  
**Email:** saddi2u@gmail.com

---

## VPC Monitoring with Flow Logs

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_3e1e79a1)

---

## Introducing Today's Project!

### What is Amazon VPC?

Amazon VPC (Virtual Private Cloud) is a service that allows you to create a logically isolated section of the AWS Cloud where you can launch AWS resources, like Amazon EC2 instances. It essentially provides a virtual network that mirrors a traditional network you might have in your own data center, but with the scalability and flexibility of the cloud.

### How I used Amazon VPC in this project

Today i discovered VPC Flow Logs which gives you insights about the network traffic entering or leaving the VPC ENIs. 

### One thing I didn't expect in this project was...

The log analysis was difficult. I did not expected that.

### This project took me...

4 hours.

---

## In the first part of my project...

### Step 1 - Set up VPCs

We are setting up VPC through wizard with minimal effort.

### Step 2 - Launch EC2 instances

We are launching EC2 Instance in our Public subnets.

### Step 3 - Set up Logs

We are here to setup VPC Flow logs to monitor our VPC traffic.

### Step 4 - Set IAM permissions for Logs

In this step we are going to grant permission to VPC Flow Logs to write logs and sent them to CloudWatch.

---

## Multi-VPC Architecture

I started my project by launching VPC wizard. I created 1 Public subnet in each of the two VPCs.

The CIDR blocks for VPCs 1 and 2 are 10.1.0.0/16 and 10.2.0.0/16. They have to be unique in order to peer with each other.

### I also launched EC2 instances in each subnet

My EC2 instances' security groups allow all SSH and ICMP traffic from anywhere 0.0.0.0/0

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_e7fa8775)

---

## Logs

Logs are like a diary for your computer systems. They record everything that happens, from users logging in to errors popping up. It's the go-to place to understand what's going on with your systems, troubleshoot problems, and keep an eye on who’s doing what.

Think of a log group as a big folder in AWS where you keep related logs together. Usually, logs from the same source or application will go into the same log group, BUT logs are region-specific. This means log data gets created and saved in the region it was created, although you can use CloudWatch dashboards to bring together logs from different regions.

### I also set up a flow log for VPC 1

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_e8398869)

---

## IAM Policy and Roles

I created an IAM policy because VPC Flow Logs by default do not have permission to record the logs and sotre them in our CloudWatch log group. This policy will grant both the permissions required for VPC Flow logs to perform those actions.

I also created an IAM role because the VPC Flow Logs requires a role (not policy). The role will have a policy attached to it for grant of required permissions.

A custom trust policy is is specific type of policy! They're different from IAM policies. While IAM policies help you define the actions a user/service can or cannot do, custom trust policies are used to very narrowly define who can use a role.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_4334d777)

---

## In the second part of my project...

### Step 5 - Ping testing and troubleshooting

We are going to test VPC peering during which both EC2 instances in our VPCs will communicate to each other. The traffic logs generated during the activity will be recorded by VPC Flow Logs and stored into CloudWatch Log Group.

### Step 6 - Set up a peering connection

In this step we are creating the VPC peering between two VPCs.

### Step 7 - Analyze flow logs

In this step we are going to review the flow logs recorded about VPC 1's public subnet.

---

## Connectivity troubleshooting

This ping response means that EC2 Instance in VPC-1 can reach to EC2 Instance in VPC-2 using its private IP address. Hence VPC Peering is working.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_99d4ba42)

In my case, VPC peering is working fine so i do not need to go through this troubleshooting step.

---

## Connectivity troubleshooting

In my case I had already configured VPC peering in my previous project including the step where you add routes in corresponding route tables of each VPC.

### To solve this, I set up a peering connection between my VPCs

I also updated both VPCs' route tables so that route tables of each VPC should know where to route the traffic. In our case, it should route the traffic to peering connection that we had created.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_7316a13d)

---

## Connectivity troubleshooting

 received ping replies from Instance 2's private IP address! This means VPC peering is successful.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_4ec7821f)

---

## Analyzing flow logs

A flow log typically includes information about network traffic, such as the source and destination IP addresses and ports, protocol, timestamps, and whether the traffic was allowed or denied. Additional details like packet and byte counts, and the flow's start and end times are also often included.

Flow logs tell us about 344 bytes of data were sent successfully from the IP address 18.237.140.165 to 10.1.5.112 using TCP protocol on port 22, with 4 packets transferred and the traffic was allowed ("ACCEPT").

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_d116818e)

---

## Logs Insights

CloudWatch Logs Insights enables you to interactively search and analyze your log data in Amazon CloudWatch Logs. You can perform queries to help you more efficiently and effectively respond to operational issues.

I ran the query was to identify top 10 talkers. This query analyzes top 10 busy source and destinations.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-networks-monitoring_3e1e79a1)

---

---
