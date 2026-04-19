# Databricks notebook source
import urllib.request
import shutil
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta

# COMMAND ----------

# Get current date
today = datetime.today()

# Calculate start month (current month - 2 months)
start_month = today - relativedelta(months=2)

# Formatting the start_month date
date = (start_month).strftime("%Y-%m")
print(date)

# COMMAND ----------

# Define and create the local directory for this date's data
dir_path = f"/Volumes/nyctaxi/00_landing/data_sources/nyctaxi_yellow/{date}"

# Define the full path for the downloaded file
local_path = f"{dir_path}/yellow_tripdata_{date}.parquet"
print(local_path)

# COMMAND ----------


try:
    # Check if the file already exists
    dbutils.fs.ls(local_path)

    # If the path already exists then set continue_downstream to no
    dbutils.jobs.taskValues.set(key="continue_downstream", value="no")
    print("File already downloaded, aborting downstream tasks")

except:
    try:
        # Construct the URL for the Parquet file corresponding to this month
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{date}.parquet"

        # Open a connection and stream the remote file
        response = urllib.request.urlopen(url)

        # Create the local directory for this date's data
        os.makedirs(dir_path, exist_ok=True)

        # Save the streamed content to the local file in binary mode
        with open(local_path, 'wb') as f:
            shutil.copyfileobj(response, f)  # Copy data from response to file

        # Set continue downstream to yes if the file was loaded
        dbutils.jobs.taskValues.set(key="continue_downstream", value="yes")
        print("File succesfully uploaded in current run!")

    except Exception as e:
        # Set continue downstream to no if the file was not loaded
        dbutils.jobs.taskValues.set(key="continue_downstream", value="no")
        print(f"File downloaded failed: {str(e)}")
        