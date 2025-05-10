from fastapi import FastAPI
from backend_handler import get_overall_user_data, get_friends_data, get_portfolio_data
from database_handler import connect_to_database

app = FastAPI()
cur = connect_to_database()

@app.get("/user/")
async def get_user_overall(user_id: str):
    person = get_overall_user_data(cur, user_id)
    return {"firstName": person.first_name, "lastName": person.last_name, "summary": person.summary, "avatarLink": person.avatar_link}
    
    
@app.get("/friends/")
async def get_friends_data(user_id: str):
    friends_objects = get_friends_data(user_id)
    friends = []
    for friend in friends_objects:
        friends.append({
            "firstName": friend.first_name,
            "lastName": friend.last_name,
            "traderProfile": "",
            "latest": "",
            "avatarLink": friend.avatar_link
        })
    return friends
    
    
@app.get("/user/details/")
async def get_user_details(user_id: str):
    portfolio = get_portfolio_data(cur, user_id)
    assets = {}
    for i, asset_name in enumerate(portfolio.asset_names):
        assets[asset_name] = portfolio.asset_amounts[i]
    return {"summary": portfolio.summary,
            "riskRatio": portfolio.risk_ratio,
            "riskText": portfolio.risk_summary,
            "totalReturn": portfolio.total_return,
            "assets": assets}