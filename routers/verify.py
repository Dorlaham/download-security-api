import base64
from fastapi import APIRouter, HTTPException
from core.logger import log_to_sqs
from utils.helpers import process_file_verification, build_log_event
from schemas.verify import VerifyResponse, VerifyRequest

router = APIRouter(prefix="/api/verify-file", tags=["verify-file"])

@router.post("/", response_model=VerifyResponse)
@log_to_sqs
async def verify_file(request: VerifyRequest):
    """
    Verifies a downloaded file based on its content and metadata.

    Returns:
        allow (bool): Whether the file is allowed or should be blocked.
    """
    try:
        magic_bytes = base64.b64decode(request.magic_bytes)
        mime_type, allow = process_file_verification(
            magic_bytes=magic_bytes,
            filename=request.filename,
            fallback_mime=request.mime
        )

        log_event = build_log_event(
            filename=request.filename,
            mime_type=mime_type,
            allow=allow,
            url=request.url
        )

        return {"allow": allow}, log_event

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
