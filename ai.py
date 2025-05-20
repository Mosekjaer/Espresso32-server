import json
import requests
from config import OPENROUTER_API_KEY

def ask_ai(indoor, outdoor):
    schema = {
        "name": "air_quality_advice",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "should_open": {
                    "type": "boolean",
                    "description": "True hvis vinduet skal åbnes"
                },
                "reason": {
                    "type": "string",
                    "description": "Forklaring på beslutningen"
                }
            },
            "required": ["should_open", "reason"],
            "additionalProperties": False
        }
    }

    request_payload = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Indendørs luftdata:\n{json.dumps(indoor, indent=2)}\n\n"
                    f"Udendørs vejrdata:\n{json.dumps(outdoor, indent=2)}\n\n"
                    "Skal jeg åbne vinduet for frisk luft? Svar i JSON."
                )
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": schema
        }
    }

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "X-Title": "Smart Air Quality",
            "Content-Type": "application/json",
        },
        json=request_payload
    )
    
    print(json.dumps(indoor, indent=2))
    print(json.dumps(outdoor, indent=2))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]

    return {
        "should_open": False,
        "reason": f"AI-fejl: {response.status_code} - {response.text}"
    }
