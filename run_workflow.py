import asyncio

from run_worker import RestaurantSuggestion
from temporalio.client import Client

async def main():
    client = await Client.connect("localhost:7233")
    
    result = await client.execute_workflow(
        RestaurantSuggestion.run, "Temporal", id="restaurant_finder_workflow", task_queue="main_task_queue"
    )