from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64

from .groq_client import generate_text
from .image_client import generate_image


@csrf_exempt
def generate(request):

    # Handle GET requests
    if request.method == "GET":
        return JsonResponse({
            "message": "AI Orchestrator API Running Successfully"
        })

    # Handle POST requests
    if request.method == "POST":

        try:
            data = json.loads(request.body)

            prompt = data.get("prompt", "")
            mode = data.get("type", "text")

            if not prompt:
                return JsonResponse({
                    "result": "Error: Prompt missing"
                }, status=400)

            # TEXT MODE
            if mode == "text":

                final_prompt = f"""
You are a helpful AI assistant.

Answer clearly and concisely.

Question:
{prompt}
"""

                answer = generate_text(final_prompt)

                return JsonResponse({
                    "result_type": "text",
                    "result": answer
                })

            # CODE MODE
            elif mode == "code":

                final_prompt = f"""
You are a coding assistant.

Return ONLY code.
Do not provide explanations.

Task:
{prompt}
"""

                answer = generate_text(final_prompt)

                return JsonResponse({
                    "result_type": "text",
                    "result": answer
                })

            # SUMMARY MODE
            elif mode == "summary":

                final_prompt = f"""
Summarize the following content in 3-4 short lines:

{prompt}
"""

                answer = generate_text(final_prompt)

                return JsonResponse({
                    "result_type": "text",
                    "result": answer
                })

            # IMAGE MODE
            elif mode == "image":

                img_bytes, error = generate_image(prompt)

                if error:
                    return JsonResponse({
                        "result_type": "text",
                        "result": f"Image Error: {error}"
                    })

                img_base64 = base64.b64encode(img_bytes).decode("utf-8")

                return JsonResponse({
                    "result_type": "image",
                    "result": f"data:image/png;base64,{img_base64}"
                })

            # DEFAULT
            else:

                answer = generate_text(prompt)

                return JsonResponse({
                    "result_type": "text",
                    "result": answer
                })

        except Exception as e:

            return JsonResponse({
                "result_type": "text",
                "result": f"Server Error: {str(e)}"
            }, status=500)

    # Handle other HTTP methods
    return JsonResponse({
        "error": "Only GET and POST methods are allowed"
    }, status=405)