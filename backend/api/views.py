from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .image_client import generate_image
from django.http import HttpResponse
import base64

from .groq_client import generate_text


@csrf_exempt
def generate(request):
    if request.method == "POST":
        data = json.loads(request.body)

        prompt = data.get("prompt", "")
        mode = data.get("type", "text")

        if not prompt:
            return JsonResponse({"result": "Error: Prompt missing"})

        # ✅ MODE ROUTING LOGIC
        if mode == "text":
            final_prompt = f"""
You are a helpful AI assistant.
Answer clearly.

Question: {prompt}
"""

        elif mode == "code":
            final_prompt = f"""
You are a coding assistant.
Return ONLY code, no explanation.

Task: {prompt}
"""

        elif mode == "summary":
            final_prompt = f"""
Summarize the following text in 3-4 short lines:

{prompt}
"""         
        elif mode == "image":
            img_bytes, error = generate_image(prompt)

            if error:
                return JsonResponse({"result": f"Image Error: {error}"})

            import base64
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")

            return JsonResponse({
                "result_type": "image",
                "result": f"data:image/png;base64,{img_base64}"
            })



        else:
            final_prompt = prompt

        # Call Groq AI
        answer = generate_text(final_prompt)

        return JsonResponse({
            "result_type": mode,
            "result": answer
        })
