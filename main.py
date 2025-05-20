from fastapi import FastAPI
from database import Base, engine, Session
from models import SensorData
from mqtt_client import start as start_mqtt

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.on_event("startup")
def on_startup():
    try:
        start_mqtt()
    except Exception as e:
        print(f"MQTT kunne ikke starte: {e}")

@app.get("/")
def root():
    return {"status": "kører"}

@app.get("/latest")
def latest():
    session = Session()
    latest_entry = session.query(SensorData).order_by(SensorData.id.desc()).first()
    session.close()
    if not latest_entry:
        return {}

    data = latest_entry.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data
