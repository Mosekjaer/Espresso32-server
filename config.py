import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_TOPIC = "sensor/data"
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
DMI_API_KEY = os.getenv("DMI_API_KEY")
STATION_ID = "06074"
EXPO_PUSH_TOKEN = os.getenv("EXPO_PUSH_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")