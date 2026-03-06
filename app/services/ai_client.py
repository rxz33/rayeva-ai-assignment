import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=api_key)


def generate_ai_response(prompt: str, max_retries: int = 2) -> str:
    last_error = None
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Return only JSON. No markdown, no explanation."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            content = completion.choices[0].message.content
            return content.replace("```json", "").replace("```", "").strip()
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(1)
    raise RuntimeError(f"AI call failed after {max_retries} attempts: {str(last_error)}")