from database_handler import get_person, get_portfolio, get_persons
from model import Person, Portfolio
from typing import List


#---------------
# This file first retrieves the data from sql and then converts it into model objects
#---------------

def get_all_persons(cur):
    persons_data = get_persons(cur)
    if not persons_data:
        return None
    persons = []
    for user_id in persons_data:
        person_data = get_overall_user_data(cur, user_id)
        persons.append(person_data)
    return persons


def get_overall_user_data(cur, user_id: str):
    person_data = get_person(cur, user_id)
    if not person_data:
        return None
        
    portfolio_data = get_portfolio_data(cur, user_id)
    
    return Person(userId=str(user_id), 
                firstName=person_data[1],
                lastName=person_data[2],
                friends=person_data[3] or [],
                avatarLink=person_data[4] or "",
                summary=person_data[5] or "",
                traderProfile=person_data[6] or "",
                latest=person_data[7] or "",
                portfolio=portfolio_data)


def get_portfolio_data(cur, user_id: str):
    portfolio_data = get_portfolio(cur, user_id)
    if not portfolio_data:
        return None
        
    return Portfolio(userId=portfolio_data[0],
                     assetNames=portfolio_data[1] or [],
                     assetAmounts=portfolio_data[2] or [],
                     tradings=portfolio_data[3] or "",
                     transactions=portfolio_data[4] or "",
                     summary=portfolio_data[5] or "",
                     totalReturn=portfolio_data[6] or 0.0,
                     riskSummary=portfolio_data[7] or "",
                     riskRatio=portfolio_data[8] or 0.0)
                     

def get_friends_data(cur, user_id: str) -> List[Person]:
    user_data = get_overall_user_data(cur, user_id)
    if not user_data or not user_data.friends:
        return []
        
    friend_objects = []
    for friend_id in user_data.friends:
        friend_data = get_overall_user_data(cur, friend_id)
        if friend_data:
            friend_objects.append(friend_data)
    return friend_objects
        