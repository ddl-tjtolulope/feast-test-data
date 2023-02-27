import feast
from joblib import dump
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Load driver order data
# orders = pd.read_csv("orders/driver_orders.csv", sep=",")
# orders["event_timestamp"] = pd.to_datetime(orders["event_timestamp"])
# orders["DRIVER_ID"] = pd.to_datetime(orders["driver_id"])

entity_df = pd.DataFrame.from_dict(
    {
        "DRIVER_ID": [1001, 1002, 1003, 1004, 1001],
        "event_timestamp": [
            datetime(2021, 4, 12, 10, 59, 42),
            datetime(2021, 4, 12, 8, 12, 10),
            datetime(2021, 4, 12, 16, 40, 26),
            datetime(2021, 4, 12, 15, 1, 12),
            datetime.now()
        ],
        "trip_completed": [1, 0, 1, 0, 1]

    }
)

# Connect to your feature store provider
fs = feast.FeatureStore(repo_path=".")

# print(orders.info())

# Retrieve training data from BigQuery
training_df = fs.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:CONV_RATE",
        "driver_hourly_stats:ACC_RATE",
        "driver_hourly_stats:AVG_DAILY_TRIPS",
    ],
).to_df()

print("----- Feature schema -----\n")
print(training_df.info())

print()
print("----- Example features -----\n")
print(training_df.head())

# Train model
target = "trip_completed"

reg = LinearRegression()
train_X = training_df[training_df.columns.drop(target).drop("event_timestamp")]
train_Y = training_df.loc[:, target]
reg.fit(train_X[sorted(train_X)], train_Y)

# Save model
dump(reg, "driver_model.bin")
