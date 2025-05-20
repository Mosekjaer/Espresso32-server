import requests
from config import DMI_API_KEY, STATION_ID

def get_dmi_observation():
    url = "https://dmigw.govcloud.dk/v2/metObs/collections/observation/items"
    params = {
        "stationId": STATION_ID,
        "period": "latest",
        "limit": 100,
        "api-key": DMI_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {}

    values = {}
    for item in response.json()["features"]:
        param = item["properties"]["parameterId"]
        values[param] = item["properties"]["value"]

    return values
