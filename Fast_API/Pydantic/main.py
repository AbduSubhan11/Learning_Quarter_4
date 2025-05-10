from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str 
    price: float

@app.post("/items")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}
