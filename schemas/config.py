from typing import List
from pydantic import BaseModel

class BlockedTypes(BaseModel):
    """
    Schema representing the configuration of blocked file types.
    """
    blocked_extensions: List[str]
    blocked_mime_types: List[str]

class UpdateBlockedTypesResponse(BlockedTypes):
    """
    Response schema returned after updating blocked types.
    Includes the updated status message.
    """
    status: str
