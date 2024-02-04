from ultralytics import YOLO
import shutil
from objectDetection.entity.config_entity import TrainingConfig
from pathlib import Path
from objectDetection.utils.common import update_datasets_dir

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
    
    def get_base_model(self):
        self.model = YOLO(
            self.config.base_model_path
        )

    @staticmethod
    def save_model(path: Path, dest_path: Path):
        # model.save(path)
        shutil.copy(path, dest_path)


    def train(self):
        
        self.model.train(data=self.config.training_data, model="yolov8n.yaml",task="detect", \
                         epochs=self.config.params_epochs,workers=8,batch=self.config.params_batch_size,imgsz=self.config.params_image_size,\
                            project=self.config.root_dir,exist_ok=True)

        self.save_model(
            path=self.config.best_model_path,
            dest_path=self.config.trained_model_path
        )