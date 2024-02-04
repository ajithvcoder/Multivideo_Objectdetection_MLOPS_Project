"""Custom TorchServe model handler for YOLOv8 models.
"""
from ts.torch_handler.base_handler import BaseHandler
import numpy as np
import base64
import torch
import io
from PIL import Image
import cv2

class_names = ['bicycle', 'bus', 'car', 'motorbike', 'person']

class ModelHandler(BaseHandler):
    """
    Model handler for YoloV8 bounding box model
    """

    img_size = 320
    """Image size (px). Images will be resized to this resolution before inference.
    """

    def __init__(self):
        # call superclass initializer
        super().__init__()

    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediction output
        :param data: Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """
        model_input = self.preprocess(data)
        # print("rank for input")
        # print(model_input.shape)
        model_output = self.inference(model_input)
        # print("model output")
        # print(model_output)
        # print(model_output[0].shape)
        return self.postprocess(model_output)



    def preprocess(self, data):
        """Converts input images to float tensors.
        Args:
            data (List): Input data from the request in the form of a list of image tensors.
        Returns:
            Tensor: single Tensor of shape [BATCH_SIZE, 3, IMG_SIZE, IMG_SIZE]
        """
        images = []


        # handle if images are given in base64, etc.
        for row in data:
            # Compat layer: normally the envelope should just return the data
            # directly, but older versions of Torchserve didn't have envelope.
            image = row.get("data") or row.get("body")
            if isinstance(image, str):
                # print(" reach str")
                # if the image is a string of bytesarray.
                image = base64.b64decode(image)

            # If the image is sent as bytesarray
            if isinstance(image, (bytearray, bytes)):
                # print(" reach bytearry")
                # image = Image.open(io.BytesIO(image))
                image = np.frombuffer(image, dtype=np.uint8)
            else:
                # if the image is a list
                # image = torch.FloatTensor(image)
                # print("reach here")
                image = image

            # force convert to tensor
            # and resize to [img_size, img_size]
            # image = transform(image)
            # print("type of image")
            # print(type(image))
            images.append(image)
        out = np.array(images)
        out = cv2.imdecode(out, cv2.IMREAD_COLOR)
        # print(out.shape)
        # convert list of equal-size tensors to single stacked tensor
        # has shape BATCH_SIZE x 3 x IMG_SIZE x IMG_SIZE
        # images_tensor = torch.stack(images).to(self.device)
        # images_tensor = images_tensor[:, :3, :, :]
        # print("########## Image tensor #######")
        # print(images_tensor.shape)

        # input_img = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)

        # Resize input image
        input_img = cv2.resize(out, (320, 320))

        # Scale input pixel values to 0 to 1
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_array = input_img[np.newaxis, :, :, :].astype(np.float32)
        return input_array

    def inference(self, data):
        ort_inputs = {self.model.get_inputs()[0].name: data}

        ort_outs = self.model.run(None, ort_inputs)
        return ort_outs

    def postprocess(self, inference_output):
        outputs = np.array(inference_output[0])
        outputs = np.transpose(outputs, (0, 2, 1))
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []

        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2], outputs[0][i][3]]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.2, 0.3, 0.5)

        detections = []
        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                'class_id': class_ids[index],
                'class_name': class_names[class_ids[index]],
                'confidence': scores[index],
                'box': [c.item() for c in box],
                'scale': self.img_size / 320}
            # print(detection)
            detections.append(detection)

        # format each detection
        return [detections]