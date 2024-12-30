from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import cv2
import threading
from violence import detect_violence
from weapons import detect_weapons
from person_detection import person_detection  # Import the updated person detection function
from sms_service import send_sms
from dotenv import load_dotenv
import os
from threading import Lock

# Load variables from .env file
load_dotenv()

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for testing purposes

# Open video or stream (use 0 for webcam or a video path for a video, or an RTSP stream link)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the video stream")
    exit()

# Store detection results
results = {"violence": False, "weapons": False, "persons": 0, "male_count": 0, "female_count": 0}
results_lock = Lock()  # Lock to ensure thread-safe access to `results`

# Function to detect violence
def detect_violence_thread(frame):
    with results_lock:
        results['violence'] = detect_violence(frame)

# Function to detect weapons
def detect_weapons_thread(frame):
    with results_lock:
        results['weapons'] = detect_weapons(frame)

# Function to detect persons and classify gender
def detect_persons_thread(frame):
    male_count, female_count = person_detection(frame)
    with results_lock:
        results['persons'] = male_count + female_count  # Total persons detected
        results['male_count'] = male_count  # Count of males
        results['female_count'] = female_count  # Count of females

# Function to capture frames continuously in the background
def capture_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            frame_bytes = jpeg.tobytes()  # Convert to bytes
            socketio.emit('video_frame', frame_bytes)  # Emit frames directly to client
            process_frame(frame)

# Function to process a frame and run detections
def process_frame(frame):
    # Create threads for detection
    violence_thread = threading.Thread(target=detect_violence_thread, args=(frame.copy(),))
    weapons_thread = threading.Thread(target=detect_weapons_thread, args=(frame.copy(),))
    persons_thread = threading.Thread(target=detect_persons_thread, args=(frame.copy(),))

    # Start the threads
    violence_thread.start()
    weapons_thread.start()
    persons_thread.start()

    # Wait for all threads to finish
    violence_thread.join()
    weapons_thread.join()
    persons_thread.join()

    # Check if both violence and weapons are detected, then send an SMS
    with results_lock:
        if results['violence'] and results['weapons']:
            message = "Alert: Violence and weapons detected on the premises. Immediate action required."
            phone_number = os.getenv('AUTHORITY_NUMBER')
            if phone_number:
                send_sms(message, phone_number)
            else:
                print("Error: AUTHORITY_NUMBER not set in environment variables.")

    # Emit detection results
    socketio.emit('detection_metrics', results)

# WebSocket connection handler to start video feed
@socketio.on('connect')
def handle_connect():
    print('Client connected, starting video feed...')
    # Start the video capture and frame processing in a background thread
    threading.Thread(target=capture_frames, daemon=True).start()

# Route to verify server is running
@app.route('/')
def index():
    return "WebSocket server is running"

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
