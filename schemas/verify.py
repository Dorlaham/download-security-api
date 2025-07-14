from pydantic import BaseModel

class VerifyRequest(BaseModel):
    """
    Request schema for verifying a downloaded file.
    """
    magic_bytes: str  # Base64-encoded file content (first bytes)
    filename: str
    mime: str         # Fallback MIME type
    url: str          # Download URL

class VerifyResponse(BaseModel):
    """
    Response schema indicating whether the file is allowed.
    """
    allow: bool
