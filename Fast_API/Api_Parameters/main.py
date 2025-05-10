from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str  = None


@app.get("/advanced/items/{item_id}")
def get_advanced_item(
    item_id: int = Path(..., title="Item ID", ge=1, description="Must be ≥ 1")
):
    return {"item_id": item_id}


@app.get("/search/")
def search_items(
    q: str | None = Query(None, min_length=3, max_length=10, title="Query string"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    return {"query": q, "skip": skip, "limit": limit}


@app.put("/update-item/{item_id}")
def update_item(
    item_id: int = Path(..., ge=1),
    item: Item = Body(..., description="Item JSON body"),
    note: str | None = Query(None, max_length=50)
):
    return {
        "item_id": item_id,
        "item": item.model_dump(),
        "note": note
    }
