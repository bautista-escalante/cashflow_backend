import os
from google import genai

def generate_gemini_response(prompt: str) -> str:
    """
    Generates a response from the Gemini API based on the provided prompt.

    Args:
        prompt (str): The input prompt to send to the Gemini API.

    Returns:
        str: The generated response from the Gemini API.
    """
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return response.text
