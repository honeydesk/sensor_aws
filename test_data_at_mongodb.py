from sensor.utils import get_collection_as_dataframe

df = get_collection_as_dataframe("aps","sensor")
print(df.head())