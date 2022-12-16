from datetime import timedelta

from feast import BigQuerySource, Entity, Feature, FeatureView, Field
from feast.types import Float32, Int64, String

trips_source = BigQuerySource(
    table="testDataset.yellow_cab",
    timestamp_field="dropoff_datetime",
    created_timestamp_column="pickup_datetime",
)

trips = Entity(
    name="yellow_cab",
    description="trips",
)

trip_costs = FeatureView(
    name="trip_costs",
    entities=[trips],
    ttl=timedelta(days=1),
    schema=[
        Field(name="fare_amount", dtype=Float32),
        Field(name="extra", dtype=Float32),
        Field(name="tip_amount", dtype=Float32),
        Field(name="tolls_amount", dtype=Float32),
    ],
    source=trips_source,
)
