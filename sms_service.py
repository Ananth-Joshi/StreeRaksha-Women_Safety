import requests
import os 
def send_sms(message, phone_number):
    """Function to send SMS using the Fast2SMS API."""
    url = "https://www.fast2sms.com/dev/bulkV2"
    querystring = {
        "authorization":os.getenv('FAST2SMS_API_KEY'),
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": phone_number
    }
    headers = {
        'cache-control': "no-cache"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            print("SMS sent successfully.")
        else:
            print(f"Error sending SMS: {response.text}")
    except Exception as e:
        print(f"Exception while sending SMS: {e}")

