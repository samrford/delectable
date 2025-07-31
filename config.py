import os
from pydantic import BaseModel

class Config(BaseModel):
    gemini_api_key: str

def get_config() -> Config:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key == None:
        raise Exception("Required env var GEMINI_API_KEY is not set")
    return Config(gemini_api_key=gemini_api_key)