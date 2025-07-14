from typing import List, Optional
from pydantic import BaseModel

class LogEntry(BaseModel):
    """
    Represents a single file download log entry.
    """
    filename: str
    mime_type: str
    allow: bool
    url: str
    timestamp: str

class LogsResponse(BaseModel):
    """
    Paginated response containing a list of log entries.
    """
    logs: List[LogEntry]
    nextCursor: Optional[str]
    has_next: bool
