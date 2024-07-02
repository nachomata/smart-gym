import paho.mqtt.client as mqtt
import json
from db_handler import DBHandler
from datetime import datetime

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "workout"

db = DBHandler()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

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
            db.add_workout(user_id, machine_id, date, repetitions, weight, duration)
            print(f"Workout added: {data}")
        else:
            print("Incomplete data in the received message")
    except Exception as e:
        print(f"Error processing the message: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()