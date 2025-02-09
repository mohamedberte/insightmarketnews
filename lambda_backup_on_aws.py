import boto3
import botocore.config
import json
import os

from datetime import datetime

def format_TwitterPost(post_brut:str)-> str:
    prompt_arn = """
        [HIDDEN]
        """

    body = {
        "prompt": f"[HIDDEN]{post_brut}",
        "max_gen_len": 500,
        #"max_tokens_to_sample": 870,
        "temperature": 0.5,  # Équilibre entre créativité et précision
        "top_p": 0.99,
        #"top_k": 250
    }

    try:
        bedrock=boto3.client("bedrock-runtime",region_name="eu-central-1",
                             config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3}))
        response=bedrock.invoke_model(body=json.dumps(body),modelId="arn:aws:bedrock:eu-central-1:664418998197:inference-profile/eu.meta.llama3-2-3b-instruct-v1:0")

        response_content=response.get('body').read()

        response_data=json.loads(response_content)

        print(response_data)

        post_formatted=response_data['generation']
        return post_formatted
    except Exception as e:
        print(f"Error generating the post:{e}")
        return ""

'''def save_blog_details_s3(s3_key, s3_bucket, post_formatted):
    s3=boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body =post_formatted )
        print("Tweets saved to s3")

    except Exception as e:
        print("Error when saving the Tweets to s3")'''

def lambda_handler(event, context):
    # event = json.loads(event['body'])  # Uncomment this line if necessary to parse event body as JSON
    
    post_brut = event['post_brut']
    post_formatted = format_TwitterPost(post_brut=post_brut)

    if post_formatted:
        # current_time = datetime.now().strftime('%H%M%S')
        # s3_key = f"post_formatted-output/{current_time}.txt"
        # s3_bucket = 'aws_bedrock_insightMarketNews'
        # save_blog_details_s3(s3_key, s3_bucket, generate_blog)
    
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain; charset=utf-8'
            },
            'body': post_formatted.encode('utf-8').decode('utf-8')
        }
    else:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain; charset=utf-8'
            },
            'body': 'Nothing is generated'
        }
