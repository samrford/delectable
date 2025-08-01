import os
from pydantic import BaseModel

class Config(BaseModel):
    gemini_api_key: str
    genai_model: str

def get_gemini_api_key() -> str:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key == None:
        raise Exception("Required env var GEMINI_API_KEY is not set")
    return gemini_api_key

def get_genai_model() -> str:
    genai_model = os.getenv("GENAI_MODEL", "gemini-2.5-flash")
    return genai_model