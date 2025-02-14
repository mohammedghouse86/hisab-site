# run_api.py
from main import get_crypto_data


# from models import store_data_in_db

def fetch_and_store_data():
    data = get_crypto_data()
    if data:
        pass
        # store_data_in_db(data)


# This will store the data in the database


if __name__ == "__main__":
    fetch_and_store_data()
