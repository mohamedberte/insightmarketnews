import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
from api import AwsApiGateWay, XPostFinanceFeatures

load_dotenv(override=True)

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
DATA_PATH = os.getenv('DATA_PATH')
AWS_API_GATEWAY_URL = os.getenv('AWS_API_GETWAY')
TOP_N = 5

def get_filename(date):
    return f"{DATA_PATH}crypto_performance_data_{date.strftime('%Y-%m-%d')}.csv"

def read_crypto_data(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    raise FileNotFoundError(f"File {filename} not found")

def get_top_performers(data):
    return data.sort_values(by='gain_percentage', ascending=False).head(TOP_N)

def prepare_post_text(top_performers, period):
    post_text = f" {period} : \n\n"
    for _, row in top_performers.iterrows():
        post_text += (
            f" * {row['name_today']} ({row['symbol_today']}):\n"
            f" Daily Return 📈 : {row['gain_percentage']:.2f}%\n"
            f" Price 💵 : ${row['price_today']:.2f}\n"
            f"📊 Volume: {row['volume_24h_today']:.2f}\n"
        )
    post_text += "----------------------------------\n"
    return post_text

def save_post_text(post_text):
    filename = f"knowledge/post/crypto_post_{datetime.today().strftime('%Y-%m-%d')}.txt"
    with open(filename, 'w') as file:
        file.write(post_text)
    return filename

if __name__ == "__main__":
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    filename_today = get_filename(today)
    filename_yesterday = get_filename(yesterday)

    crypto_data_today = read_crypto_data(filename_today)
    crypto_data_yesterday = read_crypto_data(filename_yesterday)

    top_performers_today = get_top_performers(crypto_data_today)
    top_performers_yesterday = get_top_performers(crypto_data_yesterday)

    post_text_today = prepare_post_text(top_performers_today, period='today_indicator')
    post_text_yesterday = prepare_post_text(top_performers_yesterday, period='yesterday_indicator')

    post_text = post_text_today + post_text_yesterday

    #save_post_text(post_text)

    aws = AwsApiGateWay(url=AWS_API_GATEWAY_URL)

    res = aws.post_data(post_text)

    print(res)
        
'''    service = XPostFinanceFeatures(consumer_key=CONSUMER_KEY,
                                   consumer_secret=CONSUMER_SECRET,
                                   access_token=ACCESS_TOKEN,
                                   access_token_secret=ACCESS_TOKEN_SECRET)
    
    service.post_long_tweet(post_text)'''