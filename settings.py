from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
PROTECTED_PATHS = ["/api/config", "/api/logs"]
REQUIRED_GROUP = "admin"
CONFIG_TABLE = "dorlaham-block-config"

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
LOGS_TABLE = os.getenv("LOGS_TABLE", "default-logs-table")
CONFIG_TABLE = os.getenv("CONFIG_TABLE", "default-config-table")

USERNAME = os.getenv("ADMIN_USERNAME")
PASSWORD = os.getenv("ADMIN_PASSWORD")

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

QUEUE_URL = os.environ.get("LOGS_QUEUE_URL")
