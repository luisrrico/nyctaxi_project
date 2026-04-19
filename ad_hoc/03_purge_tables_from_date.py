# Databricks notebook source
# Update this so that the date is the start of the month that was 2 months prior to the current date
from pyspark.sql import functions as F

date_from = (
    spark.range(1)
    .select(F.trunc(F.add_months(F.current_date(), -2), "month").alias("fecha"))
    .collect()[0]["fecha"]
)

print(date_from)

# COMMAND ----------

from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "nyctaxi.`01_bronze`.yellow_trips_raw")

dt.delete(f"tpep_pickup_datetime >= {date_from}")

# COMMAND ----------

from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "nyctaxi.`02_silver`.yellow_trips_cleansed")

dt.delete(f"tpep_pickup_datetime >= {date_from}")

# COMMAND ----------

from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "nyctaxi.`02_silver`.yellow_trips_enriched")

dt.delete(f"tpep_pickup_datetime >= {date_from}")

# COMMAND ----------

from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "nyctaxi.`03_gold`.daily_trip_summary")

dt.delete(f"pickup_date >= {date_from}")
