from fastapi import FastAPI
from pydantic import BaseModel
from model import Person
from backend_handler import get_overall_user_data, get_friends
from database_handler import connect_to_database

app = FastAPI()
cur = connect_to_database()

@app.get("/user/")
async def get_user_overall(user_id: str):
    person = get_overall_user_data(cur, user_id)
    return {"firstName": person.first_name, "lastName": person.last_name, "summary": person.summary, "avatarLink": person.avatar_link}
    
    
@app.get("/friends/")
async def get_friends_data(user_id: str):
    friends_objects = get_friends(user_id)
    friends = []
    for friend in friends_objects:
        friends.append({
            "firstName": friend.first_name,
            "lastName": friend.last_name,
            "traderProfile": "",
            "latest": "",
            "avatarLink": friend.avatar_link
        })
    friends.append({"friendUser1": {
        "firstName": "Alexander", 
        "lastName": "Feix",
        "traderProfile": "ai summary from trader profile",
        "latest": "latest ai summary",
        "avatarLink": "avatar/lnik"
        }})
    return friends
    
    
@app.get("/user/details/")
async def get_user_details(user_id: str, category: str):
    return {"summary": "test-summary",
            "riskRatio": 3.0,
            "riskText": "risk is risky",
            "totalReturn": 100.0,
            "assets": {"TEST_ASSET_NAME": 67.0, "TEST_ASSET_2": 23.0}}