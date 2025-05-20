import json
from paho.mqtt.client import Client
from config import MQTT_BROKER, MQTT_PASSWORD, MQTT_TOPIC, MQTT_USERNAME, EXPO_PUSH_TOKEN
from dmi import get_dmi_observation
from ai import ask_ai
from database import Session
from models import SensorData
from notifications import send_push_notification
from models import AirQualityAdvice

mqtt_client = Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Forbundet til MQTT-broker.")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Kunne ikke oprette forbindelse. Fejlkode: {rc}")

def on_message(client, userdata, msg):
    try:
        indoor_data = json.loads(msg.payload.decode())
        outdoor_data = get_dmi_observation()
        ai_response = ask_ai(indoor_data, outdoor_data)
        
        print("Du skal åbne vindue:", ai_response.should_open)
        print("AI siger:", ai_response.reason)
        
        session = Session()
        entry = SensorData(
            **indoor_data,
            should_open=int(ai_response.should_open),
            reason=ai_response.reason
        )
        session.add(entry)
        session.commit()
        
        session.close()
        
        if ai_response.should_open:
            send_push_notification(
                EXPO_PUSH_TOKEN,
                title="Tid til at lufte ud!",
                body=ai_response.reason
            )

    except Exception as e:
        print(f"Fejl ved behandling af besked: {e}")

def start():
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.tls_set()
    mqtt_client.connect(MQTT_BROKER, 8883, 60)
    mqtt_client.loop_start()
    print("MQTT-klient startet.")
