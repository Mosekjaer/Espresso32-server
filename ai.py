import json
import requests
from config import OPENROUTER_API_KEY
import re

def extract_json_from_markdown(text):
    # Matcher både ```json og ``` uden sprog
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return text  # fallback: prøv at parse hele teksten

def ask_ai(indoor, outdoor):
    request_payload = {
        "model": "qwen/qwen3-32b:free",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Her er data fra min lejlighed:\n{json.dumps(indoor, indent=2)}\n\n"
                    f"Her er lidt om vejret udenfor:\n{json.dumps(outdoor, indent=2)}\n\n"
                    "Giv mig en vurdering af indeklimaet baseret på de indendørs målinger. "
                    "Fokuser især på CO2, temperatur og luftfugtighed. "
                    "Returner *kun* et JSON-objekt med følgende format:\n"
                    "{\n"
                    '  "should_open": true,\n'
                    '  "reason": "Fordi CO2 er for høj og temperature samtluftfugtigheden lav."\n'
                    "}"
                )
            }
        ]
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

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        cleaned = extract_json_from_markdown(content)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError(f"Kunne ikke parse AI-svar som JSON:\n{content}")

    raise Exception(f"API-fejl: {response.status_code} - {response.text}")
