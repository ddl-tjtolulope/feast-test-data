import pandas as pd
import feast
from joblib import load


class DriverRankingModel:
    def __init__(self):
        # Load model
        self.model = load("driver_model.bin")

        # Set up feature store
        self.fs = feast.FeatureStore(repo_path="/repos/feast-snowflake")

    def predict(self, driver_ids):
        # Read features from Feast
        driver_features = self.fs.get_online_features(
            entity_rows=[{"DRIVER_ID": driver_id} for driver_id in driver_ids],
            features=[
                "driver_hourly_stats:CONV_RATE",
                "driver_hourly_stats:ACC_RATE",
                "driver_hourly_stats:AVG_DAILY_TRIPS",
            ],
        )
        df = pd.DataFrame.from_dict(driver_features.to_dict())

        # Make prediction
        df["prediction"] = self.model.predict(df[sorted(df)])

        # Choose best driver
        best_driver_id = df["DRIVER_ID"].iloc[df["prediction"].argmax()]

        # return best driver
        return best_driver_id


def predict(drivers):
    print("-------")
    print(f"drivers: {drivers}")
    print("-------")


    model = DriverRankingModel()
    best_driver = model.predict(drivers)
    print("-------")
    print(f"best driver: {best_driver}")
    print("-------")
    return dict(driver= str(best_driver))


if __name__ == "__main__":
    drivers = [1001, 1002, 1003, 1004]
    model = DriverRankingModel()
    best_driver = model.predict(drivers)
    print(best_driver)
