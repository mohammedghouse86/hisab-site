from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from run_api import Crypto  # Import the Crypto model

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch API key and URL from environment variables
COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')
COINMARKETCAP_API_URL = os.getenv('COINMARKETCAP_API_URL')

# Database connection
engine = create_engine("sqlite:///crypto_data.db")
Session = sessionmaker(bind=engine)

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

@app.route('/crypto')
def crypto_prices():
    """
    Endpoint to fetch and return cryptocurrency data.
    """
    data = get_crypto_data()
    if data and 'data' in data:
        result = []
        for coin in data['data']:
            coin_info = {
                'name': coin['name'],
                'price': coin['quote']['USD']['price'],
                'volume_change_24h': coin['quote']['USD']['volume_change_24h']
            }
            result.append(coin_info)
        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to fetch data from CoinMarketCap'}), 500

@app.route('/stored_data')
def get_stored_data():
    """
    Endpoint to check if any data is stored in the database.
    """
    session = Session()
    results = session.query(Crypto).all()
    session.close()

    if not results:
        return jsonify({'message': 'No data found in the database'}), 404

    data_list = []
    for entry in results:
        data_list.append({
            'name': entry.name,
            'price': entry.price,
            'volume_change_24h': entry.volume_change_24h
        })

    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)
