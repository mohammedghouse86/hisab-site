# run_api.py
import time
import schedule
from main import get_crypto_data


# from models import store_data_in_db

def fetch_and_store_data():
    """
    Fetch crypto data and store it in the database.
    """
    print("Fetching crypto data...")
    data = get_crypto_data()
    if data:
        print("Storing data in the database...")
        # store_data_in_db(data)
        print("Data stored successfully!")
    else:
        print("Failed to fetch data from CoinMarketCap")


# Schedule the function to run every day
schedule.every().day.do(fetch_and_store_data)

# Keep the script running
if __name__ == "__main__":
    print("Scheduler started. Waiting for the next run...")
    while True:
        schedule.run_pending()
        time.sleep(1)  # Wait for 1 second before checking the schedule again
