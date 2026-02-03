import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def transform_hustle_to_cv(raw_text: str):
    try:
        # Switching to 'free' to ensure credits aren't the issue during integration
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free", 
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional CV writer. Transform informal work into professional bullet points."
                },
                {"role": "user", "content": raw_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"