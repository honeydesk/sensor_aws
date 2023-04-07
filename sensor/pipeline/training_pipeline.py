from sensor.exception import SensorException
from sensor.logger import logging as  logger
from sensor.entity.config_entity import (DataIngestionConfig,
TrainingPipelineConfig,DataValidationConfig,
DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig)
from sensor.entity.artifact_entity import (DataIngestionArtifact,
DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,
ModelEvaluationArtifact,ModelPusherArtifact)
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
import os,sys


class TrainingPipeline:    
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.training_pipeline_config: TrainingPipelineConfig = training_pipeline_config

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=data_validation_config)

            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                     data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=model_trainer_config
)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_evaluation(self, data_ingestion_artifact, data_transformation_artifact, model_trainer_artifact) -> ModelEvaluationArtifact:
        try:
            model_eval_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            model_eval = ModelEvaluation(model_eval_config=model_eval_config,
                                         data_ingestion_artifact=data_ingestion_artifact,
                                         data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_artifact=model_trainer_artifact
                                        )
        
            return model_eval.initiate_model_evaluation()
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_model_pusher(self,data_transformation_artifact: DataTransformationArtifact, model_trainer_artifact: ModelTrainerArtifact):
        try:

            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                       data_transformation_artifact=data_transformation_artifact,
                                       model_trainer_artifact=model_trainer_artifact
                                       )
            return model_pusher.initiate_model_pusher()
        except Exception as e:
            raise SensorException(e, sys)