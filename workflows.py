from temporalio import workflow
from model import SearchRequest, SearchResponse, DishWithInfo
from activities import find_dishes, find_restaurants, FindDishesParams, FindRestaurantsParams
from datetime import timedelta
from pydantic import BaseModel
import asyncio

class RestaurantSuggestionParams(BaseModel):
    request: SearchRequest

@workflow.defn
class RestaurantSuggestion:
    @workflow.run
    async def run(self, params: RestaurantSuggestionParams) -> SearchResponse:
        find_dishes_output = await workflow.execute_activity(
            find_dishes,
            FindDishesParams(
                dishes=params.request.dishes,
                dish_count=params.request.dish_count,
            ),
            start_to_close_timeout=timedelta(seconds=50)
        )
        
        tasks = [
            workflow.execute_activity(
                find_restaurants,
                FindRestaurantsParams(
                    dish_name=dish,
                    location=params.request.location
                ),
                start_to_close_timeout=timedelta(seconds=50),
            )
            for dish in find_dishes_output
        ]

        restaurant_outputs = await asyncio.gather(*tasks)

        restaurants_found = [
            DishWithInfo(name=dish, where_to_find=restaurants)
            for dish, restaurants in zip(find_dishes_output, restaurant_outputs)
        ]

        return SearchResponse(dishes=restaurants_found)