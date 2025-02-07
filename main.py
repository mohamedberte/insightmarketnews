import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from api import XPostFinanceFeatures

load_dotenv(override=True)

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
DATA_PATH = os.getenv('DATA_PATH')
TOP_N = 5

def get_today_filename():
    today_date = datetime.today().strftime('%Y-%m-%d')
    return f"{DATA_PATH}crypto_performance_data_{today_date}.csv"

def read_crypto_data(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        raise FileNotFoundError(f"File {filename} not found")

def get_top_performers(data):
    sorted_data = data.sort_values(by='gain_percentage', ascending=False)
    return sorted_data.head(TOP_N)

def prepare_post_text(top_performers):
    today_date = datetime.today().strftime('%Y-%m-%d')
    post_text = f"🚀 Top {TOP_N} Crypto Performances Today ({today_date}) 🚀\n\n"
    for index, row in top_performers.iterrows():
        post_text += (
            f" * {row['name_today']} ({row['symbol_today']}):\n"
            f" Daily Return 📈 : {row['gain_percentage']:.2f}%\n"
            f" Price 💵 : ${row['price_today']:.2f}\n"
            f"📊 Volume: {row['volume_24h_today']:.2f}\n"
        )
    post_text += (
        "Please note that we are not responsible for any financial decisions made based on this information.\n"
        "#Crypto #TopPerformers #CryptoMarket #CryptoNews"
    )
    return post_text

def save_post_text(post_text):
    today_date = datetime.today().strftime('%Y-%m-%d')
    filename = f"knowledge/post/crypto_post_{today_date}.txt"
    with open(filename, 'w') as file:
        file.write(post_text)
    return filename

def read_post_text(filename):
    with open(filename, 'r') as file:
        return file.read()

def post_to_twitter(text, service):
    service.post_tweet(text)

if __name__ == "__main__":
    filename = get_today_filename()
    crypto_data = read_crypto_data(filename)
    top_performers = get_top_performers(crypto_data)
    post_text = prepare_post_text(top_performers)
        
    service = XPostFinanceFeatures(consumer_key=CONSUMER_KEY,
                                   consumer_secret=CONSUMER_SECRET,
                                   access_token=ACCESS_TOKEN,
                                   access_token_secret=ACCESS_TOKEN_SECRET)
    
    service.post_long_tweet(post_text)