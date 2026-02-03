import os
from openai import OpenAI
from dotenv import load_dotenv

# This looks for the .env file in the backend folder
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def transform_hustle_to_cv(raw_text: str):
    """
    The core 'magic'—converts informal hustle into professional bullet points.
    """
    try:
        response = client.chat.completions.create(
            # Using Gemini Flash via OpenRouter: fast and cheap for testing
            model="google/gemini-2.0-flash-001", 
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional CV writer. Transform informal work descriptions into high-impact, professional CV bullet points."
                },
                {"role": "user", "content": raw_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"