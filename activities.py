from temporalio import activity

from model import RestaurantInfo
from config import get_gemini_api_key, get_genai_model
from pydantic import BaseModel

SEARCH_PROMPT_TEMPLATE = """Give me the names (only the name, not the description or ingredients) of {dish_count} dishes that 
                            would appeal to someone who's favourite dishes are the following: {ingredient_list}. 
                            Try to be varied, finding dishes that have similar tastes/texture/spiciness to the requested dishes.
                            Separate the names using the | symbol"""

RESTAURANT_PROMPT_TEMPLATE = """Find a restaurant that serves {dish_name} in or near {location}.
	format your response like this, replacing the placeholders with the relevant information.
	If you can't find any particular field, replace it with "None found":
	[restaurant name]|[website]|[telephone no.]|[address]|[bool indicating whether takes reservations]"""

class FindDishesParams(BaseModel):
    dishes: list[str]
    dish_count: int
    
class FindRestaurantsParams(BaseModel):
    dish_name: str
    location: str

@activity.defn
async def find_dishes(params: FindDishesParams) -> list[str]:
    import google.genai as genai
    prompt = SEARCH_PROMPT_TEMPLATE.format(dish_count = params.dish_count,
                                           ingredient_list = str.join(",",params.dishes))
    ai_client = genai.Client(api_key=get_gemini_api_key())
    
    response = ai_client.models.generate_content(model=get_genai_model(), contents=prompt)
    return str.split(response.text, "|")
    
@activity.defn
async def find_restaurants(params: FindRestaurantsParams) -> RestaurantInfo:
    import google.genai as genai
    prompt = RESTAURANT_PROMPT_TEMPLATE.format(dish_name = params.dish_name, location = params.location)
    ai_client = genai.Client(api_key=get_gemini_api_key())
    
    response = ai_client.models.generate_content(model=get_genai_model(), contents=prompt)
    info = str.split(response.text, "|")
    
    return RestaurantInfo(
        name=info[0],
        website=info[1],
        telephone=info[2],
        address=info[3],
        takes_reservations=info[4]
    )