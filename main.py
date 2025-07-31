from google import genai
import uvicorn
from fastapi import FastAPI
from model import SearchRequest, SearchResponse
from service import dish_search
from config import get_config

config = get_config()
client = genai.Client(api_key=config.gemini_api_key)

app = FastAPI()

@app.post("/search")
def search(request: SearchRequest) -> SearchResponse:
    return dish_search(request, client)

if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8787, reload=True)