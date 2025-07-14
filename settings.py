import os

# Configuration
PROTECTED_PATHS = ["/api/config", "/api/logs"]
REQUIRED_GROUP = "admin"

# Secrets
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-if-needed")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

# AWS cognito
COGNITO_REGION = "eu-west-1"
USERPOOL_ID = "eu-west-1_uj0x1RCWC"
APP_CLIENT_ID = "7nq6vuoqq12tjbv9sson7lceb3"
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USERPOOL_ID}/.well-known/jwks.json"

# AWS Settings
REGION = os.getenv("REGION", "eu-west-1")
LOGS_TABLE = os.getenv("LOGS_TABLE", "dorlaham-download-logs")
CONFIG_TABLE = os.getenv("CONFIG_TABLE", "dorlaham-block-config")

QUEUE_URL = os.getenv("LOGS_QUEUE_URL")

print("✅ ENV DEBUG:", {
    "LOGS_QUEUE_URL": os.getenv("LOGS_QUEUE_URL"),
    "CONFIG_TABLE": os.getenv("CONFIG_TABLE"),
    "REGION": os.getenv("REGION")
})