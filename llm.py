
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a professional data analyst.

Your job is to answer ONLY the user's final data-analysis question.

Rules:
- Think carefully.
- If calculations are required, explain internally.
- Return ONLY the answer.
- Never wrap your response in markdown.
- Output must be valid JSON.
- The JSON should match exactly the shape requested by the user.
"""


def solve_question(question: str):
    """
    Returns a Python dictionary that becomes the 'answer' field.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        result = response.choices[0].message.content

        try:
            return json.loads(result)
        except Exception:
            return {
                "result": result
            }

    except Exception as e:
        return {
            "error": str(e)
        }
