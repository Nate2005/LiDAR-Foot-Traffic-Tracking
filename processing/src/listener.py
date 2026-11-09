import os
import sqlite3
import paho.mqtt.client as mqtt

DB_PATH = "/data/app.db"
MQTT_USER = "processor"
MQTT_PASS = os.environ["MQTT_PASS"]

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected:", reason_code)
    client.subscribe("esp32/#")   # re-subscribes automatically after reconnects

def on_message(client, userdata, msg):
    try:
        value = float(msg.payload.decode())
    except ValueError:
        print("Ignoring non-numeric payload on", msg.topic)
        return
    sensor = msg.topic.split("/", 1)[1]
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA busy_timeout=5000;")
    conn.execute("INSERT INTO readings (sensor, value) VALUES (?, ?)", (sensor, value))
    conn.commit()
    conn.close()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883)
client.loop_forever()