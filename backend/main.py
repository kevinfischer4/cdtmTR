from fastapi import FastAPI
from pydantic import BaseModel
from model import Person

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong 🏓"}


@app.post("/people/")
async def create_person(person: Person):
    return {"message": f"Person {person.first_name} created", "data": person}


@app.post("/items/")
async def create_item(item: Item):
    return {"received": item}
