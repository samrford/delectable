import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_dishes, find_restaurants
from workflows import RestaurantSuggestion

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    worker = Worker(
        client, task_queue="main_task_queue", workflows=[RestaurantSuggestion], activities=[find_dishes, find_restaurants])
    await worker.run()
    

if __name__ == "__main__":
    asyncio.run(main())