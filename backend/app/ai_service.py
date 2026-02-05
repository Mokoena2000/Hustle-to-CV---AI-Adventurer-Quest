import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# SET THIS TO True if OpenRouter is still failing with 401
USE_MOCK = False 

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def transform_hustle_to_cv(raw_text: str):
    if USE_MOCK:
        return (
            "PROFESSIONAL SUMMARY\n"
            "• Optimized logistical routes and vehicle maintenance schedules.\n"
            "• Managed high-volume cash transactions with 100% accuracy.\n"
            "• Provided exceptional customer service in fast-paced environments."
        )

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free", 
            messages=[
                {"role": "system", "content": "You are a professional CV writer. Transform informal hustle into professional bullet points."},
                {"role": "user", "content": raw_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"