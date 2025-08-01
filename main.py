import uvicorn
from fastapi import FastAPI
from model import SearchRequest, SearchResponse

from workflows import RestaurantSuggestionParams
from run_worker import RestaurantSuggestion
from temporalio.client import Client

app = FastAPI()


@app.post("/search")
async def search(request: SearchRequest) -> SearchResponse:
    temporal_client = await Client.connect("localhost:7233")

    result = await temporal_client.execute_workflow(
        RestaurantSuggestion.run,
        RestaurantSuggestionParams(
            request=request,
        ),
        id="restaurant_finder_workflow",
        task_queue="main_task_queue",
    )

    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8787, reload=True)