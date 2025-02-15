# main.py

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from run_api import Crypto  # Import Crypto model (fixed)
from utils import get_crypto_data  # Import from utils

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection
engine = create_engine("sqlite:///crypto_data.db")
Session = sessionmaker(bind=engine)

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
                'token_name': coin['name'],
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
            'token_name': entry.token_name,
            'price': entry.price,
            'volume_change_24h': entry.volume_change_24h,
            'timestamp': entry.timestamp
        })

    return jsonify(data_list)


@app.route('/debug')
def debug():
    try:
        import schedule
        return jsonify({"message": "Schedule is installed", "file": str(schedule.__file__)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
