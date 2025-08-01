from pydantic import BaseModel

class SearchRequest(BaseModel):
    dishes: list[str]
    dish_count: int
    location: str
    
class RestaurantInfo(BaseModel):
    name: str
    website: str
    telephone: str
    address: str
    takes_reservations: str
    
class DishWithInfo(BaseModel):
    name: str
    where_to_find: RestaurantInfo
    
class SearchResponse(BaseModel):
    dishes: list[DishWithInfo]