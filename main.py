from fastapi import FastAPI
from routers import config, logs, verify
from auth.middleware import verify_token
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from slowapi.middleware import SlowAPIMiddleware
from utils.limiter_config import limiter

app = FastAPI(
    title="Checkpoint Download Guard – Management API",
    version="1.0.0",
    description="""
    Provides an authenticated portal for managing file download rules and viewing download logs.

    Features:
    - View logs of downloaded files and their block/allow status
    - Configure which MIME types should be blocked by the Chrome extension
    """,
    contact={},
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

# הרשאות CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # או ספציפי בהמשך
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

public_paths = [
        "/api/auth/login",
        "/api/verify-file/",
    ]

@app.middleware("http")
async def jwt_middleware(request, call_next):
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)
    return await verify_token(request, call_next)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# חיבור router
app.include_router(logs.router)
app.include_router(config.router)
app.include_router(verify.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
