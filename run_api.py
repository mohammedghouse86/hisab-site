import time
import schedule
from main import get_crypto_data
from sqlalchemy import create_engine, Column, Integer, String, Float
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
                volume_change_24h=coin['quote']['USD']['volume_change_24h']
            )
            session.add(crypto_entry)  # Add new record
        session.commit()  # Save changes to database
        session.close()  # Close session
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
