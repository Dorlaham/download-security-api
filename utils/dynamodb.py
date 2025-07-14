import json
from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from settings import REGION, LOGS_TABLE, CONFIG_TABLE

dynamodb = boto3.resource("dynamodb", region_name=REGION)


async def get_logs(limit=100, last_evaluated_key=None):
    """
    Retrieves paginated logs from the DynamoDB logs table.

    Args:
        limit (int): Max number of items to fetch.
        last_evaluated_key (dict): Key for pagination.

    Returns:
        dict: Contains 'logs', 'nextCursor', and 'has_next'.
    """
    table = dynamodb.Table(LOGS_TABLE)

    query_kwargs = {
        "KeyConditionExpression": Key("log_id").eq("user_logs"),
        "Limit": limit,
        "ScanIndexForward": False
    }

    if last_evaluated_key:
        query_kwargs["ExclusiveStartKey"] = last_evaluated_key

    response = table.query(**query_kwargs)
    items = response.get("Items", [])
    next_key = response.get("LastEvaluatedKey")

    return {
        "logs": items,
        "nextCursor": next_key,
        "has_next": bool(next_key)
    }

async def get_block_config():
    """
    Retrieves the current block configuration from DynamoDB.

    Returns:
        dict: Blocked extensions and MIME types.
    """
    table = dynamodb.Table(CONFIG_TABLE)
    response = table.get_item(Key={"id": "config"})
    return response.get("Item")

async def update_block_config(extensions: List[str], mime_types: List[str]):
    """
    Updates the block configuration in DynamoDB.

    Args:
        extensions (List[str]): File extensions to block.
        mime_types (List[str]): MIME types to block.
    """
    table = dynamodb.Table(CONFIG_TABLE)
    table.put_item(Item={
        "id": "config",
        "blocked_extensions": extensions,
        "blocked_mime_types": mime_types
    })
