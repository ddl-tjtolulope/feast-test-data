## Domino feature store sample workflow: select the driver based on the performance


## Section 1 - Set up the feature store

### Set up the feature store using snowflake offline store and online store
https://dominodatalab.atlassian.net/wiki/spaces/~802751909/pages/2042331195/Datasources+and+Where+to+Find+Them#Snowflake
Note, raw data has been added to the Snow flake data source FEAST database table DRIVER_STATS


## Section 2 - Enable feature store to a demo project


## Section 3 - Define and publish features

Start a workspace, access the mounted feast git repo, add the feature definitions and publish the features
https://github.com/ddl-joyce-zhao/feast-test-data/blob/main/feast-snowflake/features.py



## Section 4 - Create the driver performance model

In the workspace, create a folder under ``/mnt/driver_stats_performance`.

Create the train script which will use the historical features.
https://github.com/ddl-joyce-zhao/feast-test-data/blob/main/driver_stats_performance/train.py

Create the predict script which will use the online features
https://github.com/ddl-joyce-zhao/feast-test-data/blob/main/driver_stats_performance/predict.py


Make sure to sync those changes to domino.


## Section 5 - Train the model

Start a job to run the `train.py` script

<p align="center">
<img src = readme_images/trainmodel.png width="800">
</p>

## Section 6 - Periodically materialize data to online store

Copy the script file https://github.com/ddl-joyce-zhao/feast-test-data/blob/main/driver_stats_performance/materialize.sh to the folder /mnt/driver_stats_performance.

Start a scheduled job to periodically materialize data to online store.

<p align="center">
<img src = readme_images/materialize.png width="800">
</p>

## Section 7 - Publish the model to use online features for prediction

Create a Model API to call the function `predict` of the file `driver_performance/predict_model.py`

In the model's Settings page, make sure adding the required environment variables

* FEAST_SNOWFLAKE_USER
* FEAST_SNOWFLAKE_PASSWORD
* FEAST_SNOWFLAKE_ONLINE_USER
* FEAST_SNOWFLAKE_ONLINE_PASSWORD

<p align="center">
<img src = readme_images/environment.png width="800">
</p>

The required environment variables can be found in the feature_store.yaml file. In the domino workspace and job, these have been set properly from user environment variables. But in the model API, they have to be set manually.

<p align="center">
<img src = readme_images/modelapi.png width="800">
</p>


## Section 8 - Model monitoring

Checked the required configuration for model monitoring, we need to create domino training set for the predict data. This can be done by adding code to `train.py` following the example from the documentation.  And upload the ground truth data to a datasource.

Feature store access is done in Model API which is already verified in `Section 7`. So there should be no problem doing model monitoring for models using features from feature store.



## To check if we can use Feature store in Domino, ask the following questions
* Does the component has required feast libraries installed?
* Does the component support imported git repos?
* Does the component support environment variables?

Currently feature store access in Domino workspace and job is smooth. There is no extra manual step as long as the feature store is enabled for the project properly.

Accessing feature store in ModelAPI requires extra steps to set up the environment variable manually. 
