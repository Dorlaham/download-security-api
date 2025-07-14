import json
from datetime import datetime, UTC
from core.detector import detect_mime_type, is_blocked

def parse_request_body(event):
    """
    Extracts relevant fields from the incoming request body.
    Handles edge cases like empty or invalid magic_bytes.
    """
    body = json.loads(event["body"])

    magic_list = body.get("magic_bytes", [])
    try:
        magic_bytes = bytes(magic_list) if isinstance(magic_list, list) and all(
            isinstance(b, int) and 0 <= b <= 255 for b in magic_list
        ) else b""
    except Exception as e:
        print(f"[WARN] Failed to parse magic_bytes: {e}")
        magic_bytes = b""

    return {
        "magic_bytes": magic_bytes,
        "filename": body.get("filename", "unknown"),
        "url": body.get("url", ""),
        "mime": body.get("mime", ""),
        "size": body.get("size", 0)
    }


def build_log_event(filename, mime_type, allow, url=""):
    """
    Creates a log dictionary with all relevant fields.
    """
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "filename": filename,
        "mime_type": mime_type,
        "allow": allow,
        "url": url
    }

def process_file_verification(magic_bytes: bytes, filename: str = "", fallback_mime: str = ""):
    """
    Detects MIME type from magic bytes (if available),
    and determines if the file should be blocked based on MIME or filename extension.
    """
    if magic_bytes:
        detected_mime = detect_mime_type(magic_bytes)
        print("magic type is - ", detected_mime)
    else:
        detected_mime = "application/octet-stream"

    allow = not is_blocked(detected_mime, filename, fallback_mime)

    return detected_mime, allow
