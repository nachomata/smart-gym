import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time
import plugwise_handler

MQTT_BROKER = "192.168.99.236"
MQTT_PORT = 1883
MQTT_WORKOUT_TOPIC = "workout"
MQTT_PLUGWISE_TOPIC = "plugwise"
MQTT_MACHINE_TOPIC = "machine"

class PLUGWISE_STATUS:
    ON = "on"
    OFF = "off"
class MACHINE_STATUS:
    BUSY = "busy"
    FREE = "free"


pw = None

def on_connect(client : mqtt.Client, userdata, flags, rc):
    client.subscribe(MQTT_PLUGWISE_TOPIC)
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg: mqtt.MQTTMessage):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        
        print(f"Received message: {data}")

        machine_id = data.get('machine_id')
        action_str = data.get('action')
        action = action_str.lower() == PLUGWISE_STATUS.ON
        
        global pw
        if pw is not None:
            plugwise_handler.set_relay(machine_id, action, pw)
        
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

def send_machine_status(machine_id, status):
    client = connect()
    payload = {
        "machine_id": machine_id,
        "status": status
    }

    payload_json = json.dumps(payload)
    result = client.publish(MQTT_MACHINE_TOPIC, payload_json)
    client.loop_start()
    result.wait_for_publish()
    client.disconnect()
    print(f"Machine status sent: {payload_json}")

if __name__ == "__main__":
    pw = plugwise_handler.plugwise.stick(plugwise_handler.PORT, lambda: print("Plugwise Ready"))
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()