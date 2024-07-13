import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

MQTT_BROKER = "192.168.99.236"
MQTT_PORT = 1883
MQTT_WORKOUT_TOPIC = "workout"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)

        user_id = data.get('user_id')
        machine_id = data.get('machine_id')
        repetitions = data.get('repetitions')
        weight = data.get('weight')
        duration = data.get('duration')
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if user_id and machine_id and repetitions:
            # db.add_workout(user_id, machine_id, date, repetitions, weight, duration)
            print(f"Workout added: {data}")
        else:
            print("Incomplete data in the received message")
    except Exception as e:
        print(f"Error processing the message: {e}")


def connect():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

def send_session_data(user_uid, repetitions, duration, machine_id):
    client = connect()
    payload = {
        "user_id": user_uid,
        "machine_id": machine_id,
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "repetitions": repetitions,
        "weight": 15,
        "duration": duration
    }

    payload_json = json.dumps(payload)
    result = client.publish(MQTT_WORKOUT_TOPIC, payload_json)
    client.loop_start()
    result.wait_for_publish()
    client.disconnect()


if __name__ == "__main__":
    client = connect()
    client.loop_forever()