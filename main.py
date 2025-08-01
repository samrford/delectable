import uvicorn
import uuid
from fastapi import FastAPI
from model import SearchRequest, SearchResponse

from workflows import RestaurantSuggestionParams, workflow
from run_worker import RestaurantSuggestion
from temporalio.client import Client, WorkflowExecutionStatus


app = FastAPI()


@app.post("/search")
async def search(request: SearchRequest) -> str:
    temporal_client = await Client.connect("localhost:7233")

    handle = await temporal_client.start_workflow(
        RestaurantSuggestion.run,
        RestaurantSuggestionParams(
            request=request,
        ),
        id=str(uuid.uuid4()),
        task_queue="main_task_queue",
    )

    return handle.id


@app.get("/result/{workflow_id}")
async def get_result(workflow_id: str) -> SearchResponse:
    temporal_client = await Client.connect("localhost:7233")

    workflow = temporal_client.get_workflow_handle(workflow_id)
    workflow_description = await workflow.describe()
    if workflow_description.status == WorkflowExecutionStatus.RUNNING:
        return SearchResponse(status="running", dishes=[])
    elif workflow_description.status != WorkflowExecutionStatus.COMPLETED:
        return SearchResponse(status="failed", dishes=[])
    else:
        result = await workflow.result()
        return result


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8787, reload=True)