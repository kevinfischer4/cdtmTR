from database_handler import add_friend, insert_portfolio
from backend_handler import get_friends_data, get_portfolio_data
from database_handler import connect_to_database, close_connection, insert_portfolio, insert_user, set_summary, set_trader_profile, set_latest, create_tables
import os
import csv
import json
import time


def create_portfolios_from_trading_data(cur, n: int):
    trading_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'data', 'trading_sample_data.csv')
    transaction_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'data', 'banking_sample_data.csv')
    
    trading_data = []
    user_ids_list = []
    i = n
    with open(trading_csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            trading_data.append(row)
            if row['userId'] not in user_ids_list:
                if i > 0:
                    user_ids_list.append(row['userId'])
                    i-=1
    
    transaction_data = []
    transaction_user_ids_list = []
    i = n
    with open(transaction_csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            transaction_data.append(row)
            if row['userId'] not in transaction_user_ids_list:
                if i > 0:
                    transaction_user_ids_list.append(row['userId'])
                    i-=1

    processed_users = []
    
    for user_id in user_ids_list:
        user_trading_data = [row for row in trading_data if row['userId'] == user_id]
        user_transaction_data = [row for row in transaction_data if row['userId'] == user_id]
        
        asset_holdings = {} 
        
        for trade in user_trading_data:
            isin = trade['ISIN']
            direction = trade['direction']
            execution_size = float(trade['executionSize'])
            
            if isin not in asset_holdings:
                asset_holdings[isin] = 0.0
            
            if direction == 'BUY':
                asset_holdings[isin] += execution_size
            elif direction == 'SELL':
                asset_holdings[isin] -= execution_size
        
        # Filter out assets with zero or negative holdings
        asset_holdings = {isin: amount for isin, amount in asset_holdings.items() if amount > 0}
        
        # Create lists for insert_portfolio
        asset_names = list(asset_holdings.keys())
        asset_amounts = [asset_holdings[isin] for isin in asset_names]
        
        # Convert user trading data to JSON string
        tradings_json = json.dumps(user_trading_data)
        
        # The transactions parameter is empty for now
        transactions_json = json.dumps(user_transaction_data)
        
        # Insert the portfolio
        if asset_names:  # Only create portfolio if user has assets
            insert_portfolio(cur, user_id, asset_names, asset_amounts, tradings_json, transactions_json)
            processed_users.append(user_id)
            print(f"Created portfolio for user {user_id} with {len(asset_names)} assets")
            time.sleep(2)
    
    return processed_users


def insert_n_users_from_trading_data(cur, n: int):
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'data', 'trading_sample_data.csv')
    
    user_ids_list = []
    i = n
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if i > 0:
                if row['userId'] not in user_ids_list:
                    user_ids_list.append(row['userId'])
                    i-=1
    
    inserted_user_ids = []
    for i in range(n):
        user_id = user_ids_list[i]
        insert_user(cur, user_id)
        inserted_user_ids.append(user_id)
    
    return inserted_user_ids


def set_user_attributes(cur, user_id: str):
    friends = get_friends_data(cur, user_id)
    portfolios = [get_portfolio_data(cur, friend.user_id).summary for friend in friends]
    set_summary(cur, user_id, [friend.user_id for friend in friends], portfolios)
    set_trader_profile(cur, user_id, get_portfolio_data(cur, user_id).tradings)
    set_latest(cur, user_id, get_portfolio_data(cur, user_id).tradings)


if __name__ == "__main__":
    cur, conn = connect_to_database()
    if cur and conn:
        create_tables(cur)
        conn.commit()
        insert_n_users_from_trading_data(cur, 20)
        user_ids = create_portfolios_from_trading_data(cur, 20)
        conn.commit()
        add_friend(cur, "00909ba7-ad01-42f1-9074-2773c7d3cf2c", "016e4ff3-91b2-490f-9c1e-a09defe004b2")
        add_friend(cur, "00909ba7-ad01-42f1-9074-2773c7d3cf2c", "01c56b98-55fa-4d8a-ae53-e55192fc9718")
        conn.commit()
        for user_id in user_ids:
            set_user_attributes(cur, user_id)
            conn.commit()
        
    close_connection(cur, conn)
        
        
        