import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_ID = "black-forest-labs/FLUX.1-dev"

API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}


def generate_image(prompt):

    if not HF_TOKEN:
        return None, "HF_TOKEN missing"

    try:

        payload = {
            "inputs": prompt
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        print("HF Status:", response.status_code)

        try:
            print("HF Response:", response.text[:500])
        except:
            pass

        if response.status_code != 200:
            return None, f"HF Error {response.status_code}: {response.text}"

        return response.content, None

    except Exception as e:
        return None, str(e)