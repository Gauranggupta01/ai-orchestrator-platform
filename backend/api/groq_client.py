import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_text(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ updated model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
