from fastapi import FastAPI, Depends, Body
from pydantic import BaseModel

app = FastAPI()

#  database
fake_db = []

# item model
class Item(BaseModel):
    name: str
    price: float

def save_item_to_db(item: Item):
    fake_db.append(item)
    return {"message": "Item saved", "item": item}

# Dependency for save
def save_dependency(item: Item = Body(...)):
    return save_item_to_db(item)

# using dependency
@app.post("/save")
def save_item(result: dict = Depends(save_dependency)):
    return result

@app.get("/items")
def get_all_items():
    return {"items": fake_db}
