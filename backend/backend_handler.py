from database_handler import get_person, get_portfolio
from model import Person, Portfolio
from typing import List

def get_overall_user_data(cur, user_id: str):
    person: tuple = get_person(cur, user_id)
    return Person(userId=user_id, 
                firstName=person[1],
                lastName=person[2],
                friends=person[3],
                avatarLink=person[4],
                description=person[5],
                portfolio=None)



def get_portfolio_data(cur, user_id: str):
    portfolio: tuple = get_portfolio(cur, user_id)
    return Portfolio(user_id=portfolio[0],
                     assetNames=portfolio[1],
                     assetAmounts=portfolio[2],
                     summary=portfolio[3],
                     totalReturn=portfolio[4],
                     riskSummary=portfolio[5],
                     riskRatio=portfolio[6],
                     totalRisk=portfolio[7],
                     tradings=portfolio[8],
                     transactions=portfolio[9])
                     
    

def get_friends_data(cur, user_id: str) -> List[Person]:
    friends: List[str] = get_overall_user_data(cur, user_id).friends
    friend_objects = []
    for friend_id in friends:
        user_data = get_overall_user_data(friend_id)
        friend_objects.append(user_data)
    return friend_objects
        

def get_user_details(user_id: str, category: str):
    return {"summary": "test-summary",
        "riskRatio": 3.0,
        "riskText": "risk is risky",
        "assets": {"TEST_ASSET_NAME": 67.0, "TEST_ASSET_2": 23.0}}