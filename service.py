from model import SearchRequest, SearchResponse, DishWithInfo, RestaurantInfo
from google import genai

GENAI_MODEL = "gemini-2.5-flash"
SEARCH_PROMPT_TEMPLATE = """Give me the names (only the name, not the description or ingredients) of {dish_count} dishes that 
                            would appeal to someone who's favourite dishes are the following: {ingredient_list}. 
                            Try to be varied, finding dishes that have similar tastes/texture/spiciness to the requested dishes.
                            Separate the names using the | symbol"""

RESTAURANT_PROMPT_TEMPLATE = """Find a restaurant that serves {dish_name} in or near {location}.
	format your response like this, replacing the placeholders with the relevant information.
	If you can't find any particular field, replace it with "None found":
	[restaurant name]|[website]|[telephone no.]|[address]|[bool indicating whether takes reservations]"""
    
def dish_search(request: SearchRequest, ai_client: genai.Client) -> SearchResponse:
    prompt = SEARCH_PROMPT_TEMPLATE.format(dish_count = request.dish_count,
                                           ingredient_list = str.join(",",request.ingredients))
    
    response = ai_client.models.generate_content(model=GENAI_MODEL, contents=prompt)
    dishes = str.split(response.text, "|")
    
    dishes_with_info = []
    for dish in dishes:
        dishes_with_info.append(
            DishWithInfo(
                name=dish,
                where_to_find=find_restaurants(dish, request.location, ai_client)
            )
        )
    
    return SearchResponse(dishes=dishes_with_info)
        
    
def find_restaurants(dish_name: str, location: str, ai_client: genai.Client) -> RestaurantInfo:
    prompt = RESTAURANT_PROMPT_TEMPLATE.format(dish_name = dish_name, location = location)
    response = ai_client.models.generate_content(model=GENAI_MODEL, contents=prompt)
    info = str.split(response.text, "|")
    
    return RestaurantInfo(
        name=info[0],
        website=info[1],
        telephone=info[2],
        address=info[3],
        takes_reservations=info[4]
    )