from sensor.exception import SensorException
from sensor.logger import logging
from sensor.predictor import ModelResolver
import pandas as pd
from sensor.utils import load_object
import os,sys
from sensor.config import TIMESTAMP
from sensor.utils import clean_dir

from sensor.entity.config_entity import BatchPredictionConfig

import numpy as np


class BatchPrediction:

    def __init__(self,batch_config:BatchPredictionConfig):
        try:
            self.batch_config=batch_config 
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_prediction(self):
        try:
            
            input_file = os.listdir(self.batch_config.inbox_dir)
            if len(input_file)==0:
                logging.info(f"No file found hence closing the batch prediction")
                return None 
            
            input_file=input_file[0]
                       
            inbox_file_path = os.path.join(self.batch_config.inbox_dir,input_file)
            outbox_file_path = os.path.join(self.batch_config.outbox_dir,f"{input_file}_{TIMESTAMP}")
            archive_file_path = os.path.join(self.batch_config.archive_dir,f"{input_file}_{TIMESTAMP}")
            
            logging.info(f"Creating model resolver object")
            model_resolver = ModelResolver(model_registry="saved_models")
            
            logging.info(f"Reading file :{inbox_file_path}")
            df = pd.read_csv(inbox_file_path)
            
            logging.info(f"Archeiving input file :{inbox_file_path}")
            df.to_csv(archive_file_path,index=False,header=True) 
            
            logging.info(f"Replaced Null values in :{inbox_file_path}")
            df.replace({"na":np.NAN},inplace=True)
                        
            logging.info(f"Loading transformer to transform dataset")
            transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
            input_feature_names =  list(transformer.feature_names_in_)
            input_arr = transformer.transform(df[input_feature_names])

            logging.info(f"Loading model to make prediction")
            model = load_object(file_path=model_resolver.get_latest_model_path())
            prediction = model.predict(input_arr)
            
            logging.info(f"Target encoder to convert predicted column into categorical")
            target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())

            cat_prediction = target_encoder.inverse_transform(prediction)

            df["prediction"]=prediction
            df["cat_pred"]=cat_prediction
            
            logging.info(f"Saving the prediction in the outbox folder")
            df.to_csv(outbox_file_path,index=False,header=True) 
            

            clean_dir(inbox_file_path)
        
        except Exception as e:
            raise SensorException(e, sys)


