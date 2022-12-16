# This is an example feature definition file

from datetime import timedelta

import pandas as pd

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    PushSource,
    RedshiftSource,
    RequestSource,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int64


# Defines a data source from which feature values can be retrieved. Sources are queried when building training
# datasets or materializing features into an online store.
trips_source = RedshiftSource(
    # The Redshift table where features can be found
    table="yellow_cab",
    # The event timestamp is used for point-in-time joins and for ensuring only
    # features within the TTL are returned
    timestamp_field="dropoff_datetime",
    # The (optional) created timestamp is used to ensure there are no duplicate
    # feature rows in the offline store or when building training datasets
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
