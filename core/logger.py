import os
import boto3
import json
from datetime import datetime
from functools import wraps
from settings import REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, QUEUE_URL
# Initialize SQS client and get queue URL from environment
sqs = boto3.client(
    "sqs",
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def log_to_sqs(func):
    """
    FastAPI decorator: logs the response to SQS.
    Expects the route handler to return (response, log_event).
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        response, log_event = await func(*args, **kwargs)

        try:
            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=json.dumps(log_event)
            )
        except Exception as e:
            print(f"[WARN] Failed to send log to SQS: {e}")

        return response

    return wrapper