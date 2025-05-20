from google import genai
from typing import Any
from config import GOOGLE_API_KEY
from models import AirQualityAdvice
import os

client = genai.Client(api_key=GOOGLE_API_KEY)

def ask_ai(indoor: dict[str, Any], outdoor: dict[str, Any]) -> AirQualityAdvice:
    prompt = (
        f"Her er data fra min lejlighed:\n{indoor}\n\n"
        f"Her er lidt om vejret udenfor:\n{outdoor}\n\n"
        "Giv mig en kort vurdering af indeklimaet baseret på de indendørs målinger.\n"
        "Fokuser især på CO2, temperatur og luftfugtighed.\n"
        "Hvis luften virker for dårlig, så sig klart om jeg bør lufte ud lige nu og hvorfor eller hvorfor ikke.\n"
        "Svar i JSON-format med felterne `should_open` (boolean) og `reason` (str)."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20", 
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": AirQualityAdvice
        },
    )

    print("Indendørs målinger:", indoor)
    print("Udendørs målinger:", outdoor)

    return response.parsed