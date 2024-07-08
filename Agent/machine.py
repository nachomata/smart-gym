import time
from nfc import read_nfc
import display as display
import requests
import binascii
from distance import count_repetitions, wait_for_resume_activity

SERVER_URL = "http://192.168.99.236:5000"
MACHINE_ID = 1

def authenticate_user(user_uid):
    global user_name, user_id
    
    url = f"{SERVER_URL}/api/authenticate"
    payload = {
        "uuid": user_uid
    }
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()
        if response.status_code == 200 and "error" not in response_data:
            user_id = response_data["id"]
            user_name = response_data["name"]
            return True
        else:
            print(f"Authentication failed: {response_data.get('error', 'Unknown error')}")
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

#user_id, machine_id, date, repetitions, weight, duration
def send_session_data(user_uid, repetitions, duration):
    url = f"{SERVER_URL}/api/workouts"
    payload = {
        "user_id": user_id,
        "machine_id": MACHINE_ID,
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "repetitions": repetitions,
        "weight": 15,
        "duration": duration
    }
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()
        if response.status_code == 201:
            return True
        else:
            print(f"Authentication failed: {response_data.get('error', 'Unknown error')}")
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
    
    
    print(f"Session data sent for user {user_uid}: {repetitions} repetitions")

# State machine states
WAIT_FOR_NFC = "WAIT_FOR_NFC"
AUTHENTICATE_USER = "AUTHENTICATE_USER"
COUNT_REPETITIONS = "COUNT_REPETITIONS"
SEND_SESSION_DATA = "SEND_SESSION_DATA"

# Initial state
current_state = WAIT_FOR_NFC
user_uid = None
user_uid_str = None
repetitions = 0
user_name = None
user_id = None
workout_start = 0
workout_end = 0
workout_duration = 0

display.setRGB(0, 255, 255)
display.setText("Starting...")

# State machine loop
while True:
    if current_state == WAIT_FOR_NFC:
        print("Waiting for NFC card...")
        display.setRGB(0, 255, 0)
        display.setText("Approach member card")
        # user_uid = read_nfc()
        user_uid = binascii.unhexlify(b'6221e100')
        if user_uid:
            user_uid_str = binascii.hexlify(user_uid).decode('utf-8')
            print(f"User UID: {user_uid_str}")
            current_state = AUTHENTICATE_USER
        else:
            time.sleep(1)

    elif current_state == AUTHENTICATE_USER:
        print(f"Authenticating user {user_uid_str}...")
        display.setRGB(255, 255, 0)
        display.setText(f"UID: {user_uid_str} Authenticating...")
        if authenticate_user(user_uid_str):
            print(f"User authenticated. ID: {user_id}, Name: {user_name}")
            display.setRGB(0, 255, 255)
            display.setText(f"Welcome {user_name}")
            time.sleep(2)
            current_state = COUNT_REPETITIONS
        else:
            print("Authentication failed.")
            display.setRGB(255, 0, 0)
            display.setText("Authentication failed")
            time.sleep(2)
            current_state = WAIT_FOR_NFC

    elif current_state == COUNT_REPETITIONS:
        print("Counting repetitions...")
        workout_start = time.time()
        repetitions = count_repetitions(user_name)
        workout_end = time.time()
        print("Finished counting")
        current_state = SEND_SESSION_DATA

    elif current_state == SEND_SESSION_DATA:
        print("Sending session data...")
        display.setText("Sending workout data...")
        display.setRGB(0, 0, 255)
        workout_duration = workout_end - workout_start
        send_session_data(user_id, repetitions, workout_duration)
        time.sleep(2)
        display.setText("Data saved")
        display.setRGB(0, 255, 0)
        time.sleep(2)
        
        resume = wait_for_resume_activity()
        if resume:
            current_state = COUNT_REPETITIONS
        else:
            user_id = None
            user_name = None
            user_uid = None
            user_uid_str = None
            current_state = WAIT_FOR_NFC

    else:
        print("Unknown state. Resetting to WAIT_FOR_NFC.")
        current_state = WAIT_FOR_NFC