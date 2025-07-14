from utils.limiter_config import limiter
from schemas.config import BlockedTypes, UpdateBlockedTypesResponse
from fastapi import APIRouter, Request
from utils.dynamodb import get_block_config, update_block_config

router = APIRouter(prefix="/api/config", tags=["Config"])

@router.get("/blocked-types", response_model=BlockedTypes)
@limiter.limit("5/minute")
async def fetch_blocked_types(request: Request):
    """
    Returns the current blocked MIME types and file extensions.
    """
    config = await get_block_config()
    return config

@router.post("/blocked-types", response_model=UpdateBlockedTypesResponse)
@limiter.limit("5/minute")
async def set_blocked_types(request: Request, data: BlockedTypes):
    """
    Updates the list of blocked MIME types and extensions.
    """
    await update_block_config(data.blocked_extensions, data.blocked_mime_types)
    return {
        "status": "updated",
        "blocked_extensions": data.blocked_extensions,
        "blocked_mime_types": data.blocked_mime_types
    }
