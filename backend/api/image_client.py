import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_image(prompt):

    if not HF_TOKEN:
        return None, "HF_TOKEN missing"

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=120
    )

    print("HF Status:", response.status_code)

    if response.status_code != 200:
        return None, response.text

    return response.content, None