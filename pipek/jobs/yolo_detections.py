import datetime
import cv2
import json
import torch 
from sqlalchemy import select
from pipek import models


def detect(image_id):
    print("detect", image_id)
    session = models.get_session()
    image = session.get(models.Image, image_id)

    print("process", image.id)
    image.status = "processing"
    image.updated_date = datetime.datetime.now()
    session.add(image)
    session.commit()

    image.status = "load model"
    image.updated_date = datetime.datetime.now()
    session.add(image)
    session.commit()

    # Load YOLOv5 model from the external directory
    yolov5_model_path = r'D:\EcoSystem\yolov5_team\yolov5'  # Update this path to your YOLOv5 directory

    image.status = "loading model"
    image.updated_date = datetime.datetime.now()
    session.add(image)
    session.commit()

    # yolov5_model = torch.hub.load(yolov5_model_path, 'custom', path=r'D:\EcoSystem\yolov5_team\yolov5\food16_weights\best.pt', source='local')
    # yolov5_model = torch.hub.load(yolov5_model_path, 'custom', path=r'D:\EcoSystem\yolov5_team\yolov5\yolov5n.pt', source='local')
    yolov5_model = torch.hub.load(yolov5_model_path, 'custom', path='yolov5n.pt')

    image.status = "loaded model success"
    image.updated_date = datetime.datetime.now()
    session.add(image)
    session.commit()

    # Read the image
    img = cv2.imread(image.path)

    # Resize image if needed (YOLOv5 typically uses 640x640 resolution)
    img_resized = cv2.resize(img, (224, 224))

    # YOLOv5 expects the image in RGB format
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

    # Perform detection
    results = yolov5_model(img_rgb)

    # Extract detection results (bounding boxes, confidence scores, etc.)
    detections = results.xyxy[0].cpu().numpy()

    # Filter detections to only 'face' if your model is multi-class
    # Assuming that the 'face' class is indexed by class id 0 (change as per your model's labels)
    face_detections = [det for det in detections if int(det[5]) == 0]  # Assuming class 0 is 'face'

    # Update the results dictionary with the number of detected faces
    results_dict = dict(faces=len(face_detections))

    # Print detection boxes for debugging
    print(face_detections)

    # Update image status and results in the database
    image.status = "completed"
    image.results = json.dumps(results_dict)
    image.updated_date = datetime.datetime.now()
    session.add(image)
    session.commit()
