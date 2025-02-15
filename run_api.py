import time
import threading
from datetime import datetime
from utils import get_crypto_data  # Import from utils, not main
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Create database connection
engine = create_engine("sqlite:///crypto_data.db")

# Define the database model
Base = declarative_base()


class Crypto(Base):
    __tablename__ = "crypto_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    volume_change_24h = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Stores UTC time when data is added


# Create the table in the database
Base.metadata.create_all(engine)

# Create a session maker
Session = sessionmaker(bind=engine)


def fetch_and_store_data():
    """
    Fetch crypto data and store it in the database.
    """
    print("Fetching crypto data...")
    data = get_crypto_data()

    if data and 'data' in data:
        session = Session()  # Start database session
        for coin in data['data']:
            crypto_entry = Crypto(
                name=coin['name'],
                price=coin['quote']['USD']['price'],
                volume_change_24h=coin['quote']['USD']['volume_change_24h'],
                timestamp=datetime.utcnow()  # Store the current UTC timestamp
            )
            session.add(crypto_entry)  # Add new record
        session.commit()  # Save changes to database
        session.close()  # Close session
        print(f"Data stored successfully at {datetime.utcnow()} UTC")
    else:
        print("Failed to fetch data from CoinMarketCap")


def run_scheduler():
    """
    Runs fetch_and_store_data() once every 24 hours (86400 seconds).
    """
    while True:
        fetch_and_store_data()
        print("Sleeping for 24 hours...")
        time.sleep(86400)  # 24 hours


# Run the scheduler in a separate thread
if __name__ == "__main__":
    print("Scheduler started. Fetching crypto data every 24 hours...")
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Keep the script running
    while True:
        time.sleep(1)
