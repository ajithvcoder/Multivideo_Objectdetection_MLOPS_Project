
from ultralytics import YOLO
import shutil
from objectDetection.entity.config_entity import EvaluationConfig
from objectDetection.utils.common import save_json
from pathlib import Path

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    
    @staticmethod
    def load_model(path: Path) -> YOLO:
        return YOLO(path)
    

    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self.results =  self.model.val(data=self.config.training_data, imgsz=self.config.params_image_size,batch=self.config.params_batch_size)

    def export_model(self):
        self.model.export(format="onnx")
        shutil.copy("artifacts/training/model.onnx", self.config.export_model_path)

    def save_score(self):
        save_json(path=Path("scores.json"), data=self.results.results_dict)
