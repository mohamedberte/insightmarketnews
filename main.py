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
TOP_N = 4

def get_filename(date):
    return f"{DATA_PATH}crypto_performance_data_{date.strftime('%Y-%m-%d')}.csv"

def read_crypto_data(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    raise FileNotFoundError(f"File {filename} not found")

def get_top_performers(data):
    return data.sort_values(by='gain_percentage', ascending=False).head(TOP_N)

def prepare_post_text(top_performers, period):
    post_text = f" {period} : \n"
    for _, row in top_performers.iterrows():
        post_text += (
            f" * {row['name_today']} ({row['symbol_today']})"
            f" - Daily Return : {row['gain_percentage']:.2f}% |"
            f" Price : ${row['price_today']:.2f} |"
            f" Volume: {row['volume_24h_today']:.2f}\n\n"
        )
    return post_text

def save_post_text(post_text, path='knowledge/post/crypto_post_'):
    filename = f"{path}{datetime.today().strftime('%Y-%m-%d')}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(post_text)
    return filename

def read_post_text(path):
    filename = f"{path}{datetime.today().strftime('%Y-%m-%d')}.txt"
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    filename_today = get_filename(today)
    filename_yesterday = get_filename(yesterday)

    crypto_data_today = read_crypto_data(filename_today)
    crypto_data_yesterday = read_crypto_data(filename_yesterday)

    top_performers_today = get_top_performers(crypto_data_today)
    top_performers_yesterday = get_top_performers(crypto_data_yesterday)

    post_text_today = prepare_post_text(top_performers_today, period='Today')
    post_text_yesterday = prepare_post_text(top_performers_yesterday, period='Yesterday')

    post_text = post_text_today + post_text_yesterday

    save_post_text(post_text, path='knowledge/post/crypto_post_')

    #aws = AwsApiGateWay(url=AWS_API_GATEWAY_URL)

    #res = aws.post_data(post_text)

    #save_post_text(res, path='knowledge/aws/crypto_post_')

    aws_post_generated = read_post_text(path='knowledge/aws/crypto_post_').replace('"', '')

    print(aws_post_generated)
        
    service = XPostFinanceFeatures(consumer_key=CONSUMER_KEY,
                                   consumer_secret=CONSUMER_SECRET,
                                   access_token=ACCESS_TOKEN,
                                   access_token_secret=ACCESS_TOKEN_SECRET)
    
    service.post_long_tweet(aws_post_generated)