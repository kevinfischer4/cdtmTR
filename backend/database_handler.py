import psycopg2
from urllib.parse import urlparse
from ai_handler import call_api, generate_portfolio_summary, generate_risk_summary, generate_friend_summary
from backend_handler import get_friends, get_portfolio_data
from typing import List

db_uri = "postgres://uaotb2ktauua4h:pada8df9c8488d372289a14dcea7d42b9b0cd9d1d011738ce8355372e7610037c@c3gtj1dt5vh48j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dddma3ir06vhdo"

result = urlparse(db_uri)
username = "uaotb2ktauua4h"
password = "pada8df9c8488d372289a14dcea7d42b9b0cd9d1d011738ce8355372e7610037c"
database = result.path.lstrip('/')
hostname = result.hostname
port = result.port

def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        print("Connection successful!")
        
        cur = conn.cursor()
        return cur
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
def close_connection(cur, conn):
    cur.close()
    conn.close()
    
    
def create_tables(cur):
    cur.execute("""CREATE TABLE Person (
        userId UUID PRIMARY KEY,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        friends TEXT[],
        avatarLink TEXT,
        summary TEXT,
        traderProfile TEXT,
        latest TEXT);""")
    cur.execute("""CREATE TABLE Portfolio (
        userId UUID PRIMARY KEY,
        assetNames TEXT[],      
        assetAmounts FLOAT8[], 
        tradings TEXT,
        transactions TEXT,
        summary TEXT,
        riskSummary TEXT,
        riskRatio FLOAT8[],
        totalRisk FLOAT8[]);""")
    cur.execute("""CREATE TABLE Tradings (
        userId UUID NOT NULL,
        executedAt TIMESTAMP NOT NULL,
        ISIN VARCHAR(20) NOT NULL,
        direction VARCHAR(20) NOT NULL,
        executionSize FLOAT8 NOT NULL,
        executionPrice FLOAT8 NOT NULL,
        currency VARCHAR(3) NOT NULL,
        executionFee FLOAT8 NOT NULL,
        type TEXT);""")
    cur.execute("""CREATE TABLE Transactions (
        userId UUID NOT NULL,
        bookingDate DATE NOT NULL,
        side VARCHAR(20) NOT NULL,
        amount FLOAT8 NOT NULL,
        currency VARCHAR(20) NOT NULL,
        type VARCHAR(20) NOT NULL,
        mcc TEXT);""")
    
    
def insert_user(cur, user_id: str):
    result = call_api("Generate a random firstname and a lastname, seperated with a comma. Only output the firstname and lastname, nothing else. Format: FIRSTNAME, LASTNAME").split(",")
    first_name = result[0]
    last_name = result[1]
    cur.execute("""
        INSERT INTO Person (
            userId,
            firstName,
            lastName,
            friends,
            avatarLink,
            summary,
            traderProfile,
            latest
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        );
    """, (
        user_id, # userId (UUID)
        first_name, # firstName
        last_name, # lastName
        [], # friends (TEXT[])
        'https://example.com/avatar.jpg', # avatarLink
        '', # summary of friend activity
        '', # traderProfile
        '' # latest
    ))


def insert_portfolio(cur, user_id: str, asset_names: List[str], asset_amounts: List[str], tradings: str, transactions: str):
    summary = generate_portfolio_summary(tradings, transactions)
    risk_summary = generate_risk_summary(tradings, transactions)
    cur.execute("""
        INSERT INTO Portfolio (
            userId,
            assetNames,      
            assetAmounts, 
            tradings,
            transactions,
            summary,
            riskSummary,
            riskRatio,
            totalRisk
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """, (
        user_id, # userId (UUID)
        asset_names,
        asset_amounts,
        tradings,
        transactions,
        summary,
        risk_summary,
        0.0,
        0.0
    ))


def add_friend(cur, user_id: str, friend_id: str):
    """
    Adds a friend_id to the 'friends' array of the specified user_id in the Person table.
    If the friends array is NULL, it initializes it first.
    """
    cur.execute("""
        UPDATE Person
        SET friends = COALESCE(friends, ARRAY[]::TEXT[]) || %s
        WHERE userId = %s;
    """, (friend_id, user_id))
    

def set_summary(cur, user_id: str, summary: str):
    """
    Updates the friend summary field for a given user_id in the Person table.
    """
    friends = get_friends(user_id)
    friend_names = [friend.first_name for friend in friends]
    friend_portfolio_summaries = []
    for friend in friends:
        portfolio_data = get_portfolio_data(cur, friend.user_id)
        friend_portfolio_summaries.append(portfolio_data.summary)
    summary = generate_friend_summary(friend_names, friend_portfolio_summaries)
    cur.execute("""
        UPDATE Person
        SET summary = %s
        WHERE userId = %s;
    """, (summary, user_id))


def set_risk_data(cur, user_id: str, risk_ratio: float, risk_text: str, total_risk: float):
    cur.execute("""
        UPDATE Portfolio
        SET riskRatio = %s
        SET riskText = %s
        SET totalRisk = %s
        WHERE userId = %s;
    """, (risk_ratio, risk_text, total_risk, user_id))
    
    
def set_avatar_link(cur, user_id: str, avatar_link: str):
    cur.execute("""
        UPDATE Portfolio
        SET avatarLink = %s
        WHERE userId = %s;
    """, (avatar_link, user_id))


def get_person(cur, user_id: str):
    """
    Retrieves all data for a person with the given user_id.
    """
    cur.execute("""
        SELECT * FROM Person
        WHERE userId = %s;
    """, (user_id,))
    person = cur.fetchone()
    return person


def get_portfolio(cur, user_id: str):
    """
    Retrieves all data for a portfolio with the given user_id.
    """
    cur.execute("""
        SELECT * FROM Portfolio
        WHERE userId = %s;
    """, (user_id,))
    portfolio = cur.fetchone()
    return portfolio


if __name__ == "__main__":
    cur = connect_to_database()
    create_tables(cur)
