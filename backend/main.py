from fastapi import FastAPI
from .backend_handler import get_overall_user_data, get_friends_data, get_portfolio_data, get_all_persons
from .database_handler import connect_to_database, add_friend
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-react-app.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
cur, conn = connect_to_database()

@app.get("/user/")
async def get_api_user_overall(user_id: str):
    print(user_id)
    person = get_overall_user_data(cur, user_id)
    return {"firstName": person.first_name, "lastName": person.last_name, "summary": person.summary, "avatarLink": person.avatar_link}
    
    
@app.get("/friends/")
async def get_api_friends_data(user_id: str):
    friends_objects = get_friends_data(cur, user_id)
    friends = []
    for friend in friends_objects:
        friends.append({
            "firstName": friend.first_name,
            "lastName": friend.last_name,
            "traderProfile": friend.trader_profile,
            "latest": friend.latest,
            "avatarLink": friend.avatar_link
        })
    return friends
    
    
@app.get("/user/details/")
async def get_api_user_details(user_id: str):
    portfolio = get_portfolio_data(cur, user_id)
    assets = {}
    for i, asset_name in enumerate(portfolio.asset_names):
        assets[asset_name] = portfolio.asset_amounts[i]
    return {"summary": portfolio.summary,
            "riskRatio": portfolio.risk_ratio,
            "riskText": portfolio.risk_summary,
            "totalReturn": portfolio.total_return,
            "assets": assets}
    
    
@app.get("/user/explore/")
async def get_api_explore_users(user_id: str):
    all_persons = [person.user_id for person in get_all_persons(cur)]
    user_friends = [friend.user_id for friend in get_friends_data(cur, user_id)] 
    recommondations = []
    for person in set([person.user_id for person in all_persons]):
        if person in user_friends or person == user_id:
            continue
        recommondations.append({
            "avatarLink": person.avatar_link, 
            "firstName": person.first_name,
            "lastName": person.last_name,
            "traderProfile": person.trader_profile
        })
    return recommondations
        
    
@app.post("/user/friend/")
async def post_api_add_friend(user_id: str, friend_id: str):
    add_friend(cur, user_id, friend_id)
    return {"status": "ok"}