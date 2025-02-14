# utils.py
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')
COINMARKETCAP_API_URL = os.getenv('COINMARKETCAP_API_URL')

def get_crypto_data():
    """
    Fetch cryptocurrency data from CoinMarketCap API.
    """
    headers = {
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
        'Accept': 'application/json'
    }
    response = requests.get(COINMARKETCAP_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
