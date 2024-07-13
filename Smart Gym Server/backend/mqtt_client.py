import paho.mqtt.client as mqtt
import json
from db_handler import DBHandler
from datetime import datetime

MQTT_BROKER = "localhost"
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

db = DBHandler()

machines_status = {}

def on_connect(client: mqtt.Client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe([(MQTT_WORKOUT_TOPIC, 0), (MQTT_MACHINE_TOPIC, 0)])

def on_message(client: mqtt.Client, userdata, msg : mqtt.MQTTMessage):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        
        print(f"Received message: {data}")

        if msg.topic == MQTT_WORKOUT_TOPIC:
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
                
        elif msg.topic == MQTT_MACHINE_TOPIC:
            machine_id = data.get('machine_id')
            status = data.get('status')
            
            global machines_status
            machines_status[machine_id] = status
            if status == MACHINE_STATUS.BUSY:
                client.publish(MQTT_PLUGWISE_TOPIC, json.dumps({"machine_id": machine_id, "action": PLUGWISE_STATUS.ON}))
            else:
                client.publish(MQTT_PLUGWISE_TOPIC, json.dumps({"machine_id": machine_id, "action": PLUGWISE_STATUS.OFF}))


    except Exception as e:
        print(f"Error processing the message: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()