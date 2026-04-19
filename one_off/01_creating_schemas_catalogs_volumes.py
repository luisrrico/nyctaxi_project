# Databricks notebook source
# Creating the catalog
spark.sql("""
          create catalog if not exists nyctaxi 
          managed location 'abfss://unity-catalog-storage@dbstoragebi2ot5xpgzw2w.dfs.core.windows.net/7405617693282004'
          """)

# COMMAND ----------

# Creating the schemas
spark.sql("create schema if not exists nyctaxi.00_landing")
spark.sql("create schema if not exists nyctaxi.01_bronze")
spark.sql("create schema if not exists nyctaxi.02_silver")
spark.sql("create schema if not exists nyctaxi.03_gold")

# COMMAND ----------

# Creating the volume
spark.sql("create volume if not exists nyctaxi.00_landing.data_sources")