# Project: Data Lake

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Project Description

In this project, you'll apply what you've learned on Spark and data lakes to build an ETL pipeline for a data lake hosted on S3. To complete the project, you will need to load data from S3, process the data into analytics tables using Spark, and load them back into S3. You'll deploy this Spark process on a cluster using AWS.

## Document Process

Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.

As Data Engineer at Sparkify I desinged a star schema model to facilitate the processes of queriying the data about the habits of the users of our music platform. The company has grown and now we want to move our data to the cloud. Amazon web services (AWS) seems to offer the best solution for a startup like Sparkify. Being in the cloud will enable us to continue to grow our business and users community withoud worrying about infrastructure problems. We want to focus on what is really important for us: offering a better experience when it comes to listen to the music.

Again, I modeled the database using the Star Schema Model but now we are taking the advantage of Apache Spark on top of a cluster powered by Amazon Elastic MapReduce, a web service that enables businesses, researchers, data analysts, and developers to easily and cost-effectively process vast amounts of data. We have got one Fact table, "songplays" along with four more Dimension tables named "users", "songs", "artists" and "time". We have also developed an automated pipeline to transfer all the informations from JSON files also stored in the cloud (Amazon Simple Storage Service or Amazon S3, in short) to the cluster using Python. Then, after processing the data we saved back the tables to a repository in S3.

## Star Schema

Amazon EMR is the industry leading cloud-native big data platform, allowing teams to process vast amounts of data quickly, and cost-effectively at scale. Using open source tools such as Apache Spark, Apache Hive, Apache HBase, Apache Flink, and Presto, coupled with the dynamic scalability of Amazon EC2 and scalable storage of Amazon S3, EMR gives analytical teams the engines and elasticity to run Petabyte-scale analysis for a fraction of the cost of traditional on-premise clusters.

This includes the following tables.

## Fact Table

1. songplays - records in event data associated with song plays i.e. records with page NextSong

## Dimension Tables

1. users - users in the app
2. songs - songs in music database
3. artists - artists in music database
4. time - timestamps of records in songplays broken down into specific units

## Spark Process

The ETL job processes the song files then the log files. The song files are listed and iterated over entering relevant information in the artists and the song folders in parquet. The log files are filtered by the NextSong action. The subsequent dataset is then processed to extract the date, time, year etc. fields and records are then appropriately entered into the time, users and songplays folders in parquet for analysis.

## Project Structure

1. etl.py - The ETL to reads data from S3, processes that data using Spark, and writes them to a new S3
2. dl.cfg - Configuration file that contains info about AWS credentials
3. test.ipynb - test script for etl.py