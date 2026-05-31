import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

print("API KEY FOUND:", API_KEY is not None)

def generate_ai_remark(risk, glucose, haemoglobin, cholesterol):

    print("AI Function Started")

    try:

        prompt = f"""
        Generate a short healthcare remark.

        Risk Level: {risk}
        Glucose: {glucose}
        Haemoglobin: {haemoglobin}
        Cholesterol: {cholesterol}

        Keep it professional and under 50 words.
        """

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=20
        )

        response.raise_for_status()

        print("AI response recieved")

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        print("OPENROUTER ERROR:", e)

        return f"Predicted Risk: {risk}"