from fastapi import Request
from fastapi.responses import JSONResponse
from auth.cognito_handler import verify_cognito_jwt_token
from settings import PROTECTED_PATHS, REQUIRED_GROUP

async def verify_token(request: Request, call_next):
    """
    Middleware to verify AWS Cognito JWT token and enforce group-based access.

    - Extracts token from Authorization header or cookie.
    - Validates the token using Cognito's JWKS.
    - Attaches user claims to request.state.user.
    - Enforces admin group access for protected paths.

    Args:
        request (Request): Incoming HTTP request.
        call_next: Next middleware or route handler.

    Returns:
        Response: Either error response or result of the next handler.
    """
    token = None
    if request.method == "OPTIONS":
        return await call_next(request)

    if "authorization" in request.headers:
        token = request.headers["authorization"].replace("Bearer ", "")
    elif "access_token" in request.cookies:
        token = request.cookies["access_token"]

    if not token:
        return JSONResponse(status_code=401, content={"detail": "Missing token"})

    user = verify_cognito_jwt_token(token)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

    request.state.user = user

    path = request.url.path
    if any(path.startswith(p) for p in PROTECTED_PATHS):
        groups = user.get("cognito:groups", [])
        if REQUIRED_GROUP not in groups:
            return JSONResponse(status_code=403, content={"detail": "Admin access required"})

    return await call_next(request)
