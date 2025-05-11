import requests
from typing import List

def call_api(prompt: str):
    # We are aware of the risks, don't blame us :D
    API_KEY = 'cxS27JBQsBfFenit5BvwlPPFSQ7DWaNw'
    url = 'https://api.mistral.ai/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "mistral-large-latest",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        summary = response.json()['choices'][0]['message']['content']
        print("Summary:\n", summary)
        return summary
    else:
        print("Error:", response.status_code, response.text)


def generate_friend_summary(friend_names: List[str], friend_portfolio_summaries: List[str]):
    instruction_prompt = f"""Your task is to generate a short summary on the provided portfolio summaries of friends of the user.
    Answer only using the first names of the friends and do not mention any money amount or currency.
    For instance, you could infer trends and investment behaviours of your friends on the provided data.
    Summarize the friend portfolios using the provided data.
    Answer shortly in max. 2 sentences.
    If you can not create a summmary of the data, answer with 'No summary available.'\n
    Here is the data: \n"""
    for i, friend_name in enumerate(friend_names):
        instruction_prompt += f"Summary of friend {friend_name}: {friend_portfolio_summaries[i]} \n\n\n"
    return call_api(instruction_prompt)
    

def generate_user_trader_profile(tradings: str):
    instruction_prompt = f"""Your task is to generate a short trader profile of the person and the provided data.
    Cosider the trading frequency, asset distrebution and other important stuff.
    Do not include currencies, money amounts, only include general information that can be inferred from the data.
    Answer shortly in max. 7 words.
    If you can not create a summmary of the data, answer with 'No summary available.'\n
    Here is the data: {tradings}"""
    return call_api(instruction_prompt)


def generate_user_latest_changes(tradings: str):
    instruction_prompt = f"""Your task is to summarize the latest activity of the user on the provided data. 
    Summarize the data very generally and do not mention any currencies or money amounts or other private data.
    Answer shortly in max. 7 words.
    If you can not create a summmary of the data, answer with 'No summary available.'\n
    Here is the data: {tradings}"""
    return call_api(instruction_prompt)


def generate_portfolio_summary(trading_data: str, transaction_data: str):
    instruction_prompt = f"""Your task is to generate a finance portfolio summary on the provided data. 
    Summarize the assets, regions and industry. 
    The data is split into trading data and transaction data.
    Do not mention any money amounts, currencies and other specific data.
    Keep the summary more general and consider deviding the data into regions, industries and other trends.
    Answer shortly in max. 4 sentences.
    If you can not create a summmary of the data, answer with 'No summary available.'\n
    Here is the trading data: {trading_data}\n\n\n
    Here is the transaction data: {transaction_data}"""
    return call_api(instruction_prompt)


def generate_risk_summary(trading_data: str, transaction_data: str):
    instruction_prompt = f"""Your task is to generate a scientific risk summary for the following data. 
    Evaluate whether the given data is risky or valid. 
    Answer generally and do not include any money amounts, currencies or other specific data.
    The answer should act more like a general overview of the validity state.
    The data is split into trading data and transaction data.
    Answer shortly in max. 3 sentences.
    If you can not create a summmary of the data, answer with 'No summary available.'\n
    Here is the trading data: {trading_data}\n\n\n
    Here is the transaction data: {transaction_data}"""
    return call_api(instruction_prompt)
    