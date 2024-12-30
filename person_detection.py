from ultralytics import YOLO
import cv2
import numpy as np
from keras.models import load_model

# Load your YOLO model
model = YOLO('yolo11s.pt')

# Load the gender classification model
gender_model = load_model('gender_model.h5')

def predict_gender(cropped_person):
    if cropped_person.size > 0:
        resized_image = cv2.resize(cropped_person, (128, 256))  # Resize to match input size of gender_model
        normalized_image = resized_image / 255.0  # Normalize pixel values to [0, 1]
        preprocessed_image = np.expand_dims(normalized_image, axis=0)  # Add batch dimension
        gender_prediction = gender_model.predict(preprocessed_image)
        confidence = gender_prediction[0][0]
        gender_label = 'Male' if confidence > 0.5 else 'Female'
        return gender_label, confidence
    return "Unknown", 0.0

def person_detection(frame):
    male_count = 0
    female_count = 0

    # Perform inference and stream results
    results_generator = model(frame, stream=True, classes=[0], device=0)  # Generator for streaming results

    for result in results_generator:  # Iterate over the generator to get each `Results` object
        if result.boxes:  # Check if any boxes are detected
            for box in result.boxes:  # Iterate over the detected boxes
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Bounding box coordinates
                confidence = box.conf[0].item()       # Confidence score
                class_id = int(box.cls[0].item())     # Class ID

                # Crop the detected person from the frame
                cropped_person = frame[y1:y2, x1:x2]

                # Predict gender
                gender_label, gender_confidence = predict_gender(cropped_person)
                print(f"Gender: {gender_label}, Confidence: {gender_confidence}")

                if gender_label == 'Male':
                    male_count += 1
                elif gender_label == 'Female':
                    female_count += 1
                    
    return male_count, female_count
