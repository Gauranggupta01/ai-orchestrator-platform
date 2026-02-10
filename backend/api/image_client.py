import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"

API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


def generate_image(prompt):
    if not HF_TOKEN:
        return None, "HF_TOKEN missing"

    payload = {
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # Debug print
    print("HF Status:", response.status_code)
    print("HF Response:", response.text[:200])

    if response.status_code != 200:
        return None, response.text

    return response.content, None
