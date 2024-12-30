from ultralytics import YOLO
import cv2

model = YOLO('weapons.pt')

def detect_weapons(frame):
    """Detect weapons in the frame and return weapon status (True/False)"""
    # Perform object detection with YOLO
    results = model(frame, device=0, classes=[1])  # Specify weapon class ID (1)

    # Check if a weapon is detected based on the results
    for result in results:  # Iterate over the results (one result per frame)
        for box in result.boxes:  # Iterate over detected boxes
            confidence = box.conf[0].cpu().numpy()  # Confidence score
            cls = int(box.cls[0].cpu().numpy())  # Class index
            
            # Check if the detected class is weapon (class ID 1)
            if cls == 1 and confidence > 0.5:  # Adjust confidence threshold as needed
                return True  # Return True if weapon is detected

    return False  # Return False if no weapon is detected
