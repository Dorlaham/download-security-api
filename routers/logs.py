from typing import Optional
from schemas.logs import LogsResponse
from utils.limiter_config import limiter
from fastapi import APIRouter, Query, Request
from utils.dynamodb import get_logs
import json

router = APIRouter(prefix="/api/logs", tags=["Logs"])

@router.get("/", response_model=LogsResponse)
@limiter.limit("5/minute")
async def fetch_logs(
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[str] = Query(None)
):
    """
    Returns a paginated list of download logs.

    Args:
        limit (int): Max number of logs to return (default: 10).
        cursor (str, optional): Encoded key for pagination.

    Returns:
        LogsResponse: A list of log entries with pagination info.
    """
    last_evaluated_key = None

    if cursor:
        try:
            last_evaluated_key = json.loads(cursor)
        except Exception:
            return {"logs": [], "nextCursor": None, "has_next": False}

    result = await get_logs(limit=limit, last_evaluated_key=last_evaluated_key)

    return {
        "logs": result["logs"],
        "nextCursor": json.dumps(result["nextCursor"]) if result["nextCursor"] else None,
        "has_next": bool(result["nextCursor"])
    }
