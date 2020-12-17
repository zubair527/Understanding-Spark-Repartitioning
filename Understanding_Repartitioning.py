# Databricks notebook source
# MAGIC %md 
# MAGIC To Understand how repartitioning works. 

# COMMAND ----------

# MAGIC %md
# MAGIC Run the below scripts/command in root of cloned repository. 

# COMMAND ----------

# Loading the csv file into a dataframe
file_path = "2015-summary.csv"

df = spark.read.format("csv").option("inferSchema", "true").option("header", "true").load(file_path)

# Print Schema
df.printSchema()

# Get the number of distinct countries in column "ORIGIN_COUNTRY_NAME", below shall print 125. 
df.agg(countDistinct(col("origin_country_name"))).show()


# Trying to create a partition for every different country name even if it has very few records. 
# Link to spark documentation about this function: https://spark.apache.org/docs/latest/api/python/_modules/pyspark/sql/dataframe.html#DataFrame.repartition
df2 = df.repartition(125, "origin_country_name")




# COMMAND ----------

# MAGIC %md  
# MAGIC Below code is creating some mis-understanding because of 2 reasons:
# MAGIC   * First, it doesn't always create 125 partitons
# MAGIC   * Second, when I get data of partitions into python list via glom().collect() it shows some empty arrays. My understading is that each partition is converted in a list in python via glom()

# COMMAND ----------

# checking number of partitions, 
df2.rdd.getNumPartitions()

# COMMAND ----------

# Getting all partitions into
df2_arry = df2.rdd.glom().collect()2

len(df2_arry)

df2_arry

# Question: As per my understanding the sub-arrays printed by df2_arry must have at-least one element. But multiple arrays are empty. 




# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Qustion: 
# MAGIC * Should not repartition() create partitions based on column name when given? 
# MAGIC * Why is it merging partitions?
# MAGIC * Is there ways to dis-able this auto-merge happending?
