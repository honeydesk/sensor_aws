import pymongo
import pandas as pd
import json
from dataclasses import dataclass
from datetime import datetime
# Provide the mongodb localhost url to connect python to mongodb.
import os

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_access_secret_key:str = os.getenv("AWS_SECRET_ACCESS_KEY")


TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url,tls=True,tlsAllowInvalidCertificates=True)
TARGET_COLUMN = "class"