from objectDetection.config.configuration import ConfigurationManager
from objectDetection.components.prepare_base_model import PrepareBaseModel
from objectDetection import logger

STAGE_NAME = "Prepare base model"

class PrepareBaseModelTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
        prepare_base_model.get_base_model()

if __name__ == "__main__":
    try:
        logger.info(f"*************************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\nx========x")
    except Exception as e:
        logger.exception(e)
        raise e