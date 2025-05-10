import os
import csv
from typing import List, Dict, Tuple
import json
import time
from database_handler import connect_to_database, close_connection, insert_portfolio

def create_portfolios_from_trading_data(cur, conn, n: int):
    """
    Creates portfolios for the first n distinct users in the trading_sample_data.csv file.
    
    For each user, it processes all their trading records to compute their current holdings
    for each asset (ISIN) and creates a portfolio entry with this data.
    
    Args:
        cur: Database cursor
        conn: Database connection
        n: Number of users to process
        
    Returns:
        List of user IDs for which portfolios were created
    """
    # Path to the CSV file
    trading_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'data', 'trading_sample_data.csv')
    transaction_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'data', 'banking_sample_data.csv')
    
    # Read all trading data
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
        # Filter trading data for this user
        user_trading_data = [row for row in trading_data if row['userId'] == user_id]
        user_transaction_data = [row for row in transaction_data if row['userId'] == user_id]
        
        # Process the user's trading data to compute asset holdings
        asset_holdings = {}  # ISIN -> current amount
        
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
    
    # Commit the changes
    conn.commit()
    
    return processed_users

def main():
    cur, conn = connect_to_database()
    if cur and conn:
        try:
            # Create portfolios for the first 10 users
            processed_users = create_portfolios_from_trading_data(cur, conn, 10)
            print(f"Successfully created portfolios for {len(processed_users)} users")
        except Exception as e:
            conn.rollback()
            print(f"An error occurred: {e}")
        finally:
            close_connection(cur, conn)

if __name__ == "__main__":
    main() 