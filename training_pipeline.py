from sensor.exception import SensorException
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.entity.config_entity import TrainingPipelineConfig
import sys

training_pipeline = TrainingPipeline(training_pipeline_config=TrainingPipelineConfig())
file_path="/config/workspace/aps_failure_training_set1.csv"
print(__name__)
if __name__=="__main__":
    try:
        data_ingestion_artifact = training_pipeline.start_data_ingestion()
        data_validation_artifact = training_pipeline.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = training_pipeline.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
        model_trainer_artifact = training_pipeline.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
        model_eval_artifact = training_pipeline.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                       data_transformation_artifact = data_transformation_artifact,
                                                                       model_trainer_artifact=model_trainer_artifact)
        if model_eval_artifact.is_model_accepted:
            training_pipeline.start_model_pusher(data_transformation_artifact=data_transformation_artifact,
                                                 model_trainer_artifact=model_trainer_artifact)
    except Exception as e:
        raise SensorException(e, sys)