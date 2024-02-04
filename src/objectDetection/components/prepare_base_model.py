from ultralytics import YOLO
import shutil
from pathlib import Path
from objectDetection.entity.config_entity import PrepareBaseModelConfig

class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
    
    def get_base_model(self):
        self.model = YOLO(self.config.params_weights)
        # print(type(self.model))
        self.save_model(path=self.config.base_model_path, model=self.model)

    
    @staticmethod
    def save_model(path: Path, model: YOLO):
        # model.export(format="")
        shutil.copy("yolov8n.pt", path)