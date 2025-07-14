import boto3
from magic import Magic
from typing import Tuple
from settings import REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, CONFIG_TABLE

# DynamoDB client
dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# MIME type detector using libmagic
magic_detector = Magic(mime=True)

def detect_mime_type(magic_bytes: bytes) -> str:
    """
    Detects the MIME type of a byte buffer using libmagic.

    Args:
        magic_bytes (bytes): File content.

    Returns:
        str: Detected MIME type, or 'application/octet-stream' if unknown.
    """
    return magic_detector.from_buffer(magic_bytes) if magic_bytes else "application/octet-stream"

def fetch_block_config() -> Tuple[list[str], list[str]]:
    """
    Fetches blocked MIME types and file extensions from DynamoDB.

    Returns:
        Tuple: (blocked MIME types, blocked file extensions)
    """
    table = dynamodb.Table(CONFIG_TABLE)
    response = table.get_item(Key={"id": "config"})
    item = response.get("Item", {})

    return item.get("blocked_mime_types", []), item.get("blocked_extensions", [])

def is_blocked(
    mime_type: str,
    filename: str = "",
    fallback_mime: str = ""
) -> bool:
    """
    Determines if a file should be blocked based on MIME type or extension.

    Args:
        mime_type (str): Primary detected MIME type.
        filename (str): Optional filename to check extension.
        fallback_mime (str): Optional fallback MIME type.

    Returns:
        bool: True if the file should be blocked, False otherwise.
    """
    blocked_mimes, blocked_exts = fetch_block_config()

    if mime_type in blocked_mimes or fallback_mime in blocked_mimes:
        return True

    if mime_type == "application/octet-stream" and filename:
        lower = filename.lower()
        return any(lower.endswith(ext) for ext in blocked_exts)

    return False
