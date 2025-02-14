from flask import Flask
import requests

app = Flask(__name__)

def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['usd']

@app.route('/bitcoin')
def bitcoin():
    price = get_bitcoin_price()
    return f"Bitcoin price: ${price}"

if __name__ == '__main__':
    app.run(debug=True)