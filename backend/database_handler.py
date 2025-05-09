from data_loader import load_banking_data, load_trading_data
import os


if __name__ == "__main__":
    load_trading_data(os.path.join(os.getcwd(), "backend", "data", "trading_sample_data.csv"))
    load_banking_data(os.path.join(os.getcwd(), "backend", "data", "banking_sample_data.csv"))
    print("Done")