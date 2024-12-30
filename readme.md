# StreeRaksha Women's Safety System
StreeRaksha is a women's safety system designed to provide real-time monitoring and alerts to ensure the safety of women in public spaces. The system utilizes surveillance cameras, advanced image processing models, and emergency alert mechanisms to identify potential risks and send immediate notifications.

## Features

-  **Real-time Surveillance**: Detects people in public areas using YOLO (You Only Look Once) object detection.

-  **Gender Classification**: Classifies detected individuals as male or female using a custom Convolutional Neural Network (CNN).

-  **Risk Assessment**: Evaluates the risk level based on the ratio of men to women, violence and weapons in the footage.

-  **SOS Alerts**: Sends alerts to authorities using Fast2SMS in case of detected distress or panic signals.

## Setup Instructions

### 1. Clone the Repository

```bash

git  clone  https://github.com/Ananth-Joshi/StreeRaksha-Women_Safety.git

cd  StreeRaksha-Women_Safety

```
### 2. Install Backend Dependencies
Ensure you have **Python 3.7+** installed and use `pip` to install the required dependencies:

```bash

pip  install  -r  requirements.txt

```

### 3. Install Frontend Dependencies

Navigate to the `frontend` folder and install the necessary dependencies for the Electron app:

```bash

cd  frontend

npm  install

```

### 4. Register for Fast2SMS API Key

To send SMS alerts through the system, you need an API key from **Fast2SMS**.

1. Go to [Fast2SMS](https://fast2sms.com/).

2. Sign up for a new account or log in to your existing account.

3. Navigate to the **API Section** of your dashboard.

4. Generate a new API key.

### 5. Set Up Environment Variables

For security, API keys should not be hardcoded into your code. Instead, store them as environment variables.

1. Create a `.env` file in the root directory of the project.S
2. Add the following lines to your `.env` file, replacing the placeholder with your actual API key from Fast2SMS:

```

FAST2SMS_API_KEY=your_fast2sms_api_key_here
AUTHORITY_NUMBER=number_to_send_SOS_message 

```

### 6. Running the Backend

Once you've set up everything, run the backend application:

```bash

python  server.py

```
This will start the system, monitor the environment through surveillance cameras, and send alerts when necessary.

### 7. Running the Frontend (Electron App)
To run the frontend application, navigate to the `frontend` folder and start the Electron app:


```bash

cd  frontend

npm  start

```
This will open the frontend in a window.
  
---
## Project Structure

```
streeRaksha/
├── frontend/                   # Contains the Electron frontend application
│   ├── (Electron files and folders)
├── models/                     # Contains the trained machine learning models
│   ├── gender_model.h5         # Model for gender classification
│   ├── violence.pt             # Model for violence detection
│   ├── weapons.pt              # Model for weapon detection
│   ├── yolo11s.pt              # YOLO model for object detection
├── .env.example                # Example environment variable configuration
├── .gitattributes              # Git LFS tracking configuration
├── .gitignore                  # Git ignore file
├── person_detection.py         # Python script for detecting persons
├── readme.md                   # This README file
├── requirements.txt            # Python dependencies
├── server.py                   # Backend server script
├── sms_service.py              # SMS service script for notifications
├── violence.py                 # Violence detection logic
├── weapons.py                  # Weapons detection logic
```

## Results


