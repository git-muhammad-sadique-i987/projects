<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Visualize data with QuickSight

**Project Link:** [View Project](http://learn.nextwork.org/projects/aws-analytics-quicksight)

**Author:** Muhammad Sadique  
**Email:** saddi2u@gmail.com

---

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-analytics-quicksight_6c7f7ef0)

---

## Introducing Today's Project!

### What is Amazon QuickSight?

To anlyze and visualize datasets.

### How I used Amazon QuickSight in this project

I connected quicksight with amazon s3 bucket which contained a dataset in csv format and a manifest.json file. I was able to import the dataset into quicksight and then i visualize the data.

### One thing I didn't expect in this project was...

How easy it was to build visuals and import the dataset.

### This project took me...

2 hours.

---

## Upload project files into S3

S3 is used in this project to store two files, which are:
1. netflix_titles.csv
2. manifest.json

I edited the manifest.json file by updating S3 URI of Netflix dataset which i'll be analysing through Amazon Quick Sight dashboard. It’s important to edit this file because keeping the old URI would cause manifest.json file to point at incorrect file

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-analytics-quicksight_3c3cd85a)

---

## Create QuickSight account

Creating a QuickSight account cost nothing as long as you complete the project during the free trial which lasts 30 days.

Creating an account took me 2 minuts. It easy peasy. Make sure to uncheck the box where it says to subscribe for add-on. It might cost you $ 500 right away.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-analytics-quicksight_f4ab4214)

---

## Download the Dataset

I connected the S3 bucket to QuickSight by visiting Dataset page.

The manifest.json file was important in this step because it tells the Quick Sight what kind of data is in there in dataset. In our case it tells that file type is CSV, the data containts the headers and delimeter is ","

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-analytics-quicksight_6f874996)

---

## My first visualization

o create visualizations on QuickSight, I selected the field i.e. release year into "Auto Graph" area of Quicksight. It automatically puts the release year onto Y-axis.
I then clicked Add to add it into the Quicksight dashboard.

The chart/graph shown here is a breakdown of movies and TV shows by "release year"

I created this graph by dragging and dropping "release year" onto "Auto Graph" area in QuickSight canvas.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-analytics-quicksight_aff3aad7)

---

## Using filters

Filters are useful for to filter the data so that the visual can focus on the data that you want to interested in. 

This visualization is a breakdown of generes that were found in "Listed In"column of the dataset. Here I added a filter by "Action & Adventure", "Thriller" and "TV Comedies". I further filtered TV shows / movies that were released in and after 2015.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-analytics-quicksight_c32248c5)

---

## Setting up a dashboard

As a finishing touch, I updated titles of each visual and turned off unneccessary legends.

Did you know you could export your dashboard as PDFs too? I did this by pulishing it first and then clicked "Export" button to export it as PDF.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-analytics-quicksight_6c7f7ef0)

---

## Refreshing source data

---

---
