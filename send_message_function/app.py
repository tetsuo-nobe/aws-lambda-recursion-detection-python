import json
import boto3
import os
import logging 

logger = logging.getLogger()
level = logging.INFO
logger.setLevel(level)

def lambda_handler(event, context):
    # SQS Client 作成
    sqsclient = boto3.client('sqs')
    
    # 環境変数の取得
    target_queue_url = os.getenv('TARGET_QUEUE_URL')
    trace_id     = os.getenv('_X_AMZN_TRACE_ID','NOT FOUND')
    
    # 受信メッセージ取得
    message = event['Records'][0]['body']
    
    # メッセージとトレース ID をログ出力
    logger.info('MESSAGE RECEIVED :: ' + message)
    logger.info("TRACE ID : " + trace_id)
    
    # メッセージに処理済のマークをつける
    message = json.loads(message)
    message['orderStatus'] = 'Processed' 
    message = json.dumps(message)  
       
    # メッセージを送信 
    logger.info('Publishing Processed Message back to SQS ...')
    response = sqsclient.send_message(
          QueueUrl=target_queue_url,
          MessageBody=message
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": message
        })
    }
