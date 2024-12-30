from ultralytics import YOLO
import cv2

model = YOLO('models/violence.pt')

def detect_violence(frame):
    """Detect violence in the frame and return violence status (True/False)"""
    # Perform object detection with YOLO
    results = model(frame, device=0, classes=[1])  # Specify violence class ID (1)

    # Check if violence is detected based on the results
    for result in results:  # Iterate over the results (one result per frame)
        for box in result.boxes:  # Iterate over detected boxes
            confidence = box.conf[0].cpu().numpy()  # Confidence score
            cls = int(box.cls[0].cpu().numpy())  # Class index
            
            # Check if the detected class is violence (class ID 1)
            if cls == 1 and confidence > 0.5:  # Adjust confidence threshold as needed
                return True  # Return True if violence is detected

    return False  # Return False if no violence is detected
