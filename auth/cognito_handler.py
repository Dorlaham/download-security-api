from jose import jwt, jwk
from jose.utils import base64url_decode
from typing import Optional
import requests
from datetime import datetime, timezone
from settings import JWKS_URL, APP_CLIENT_ID

# Cached JWKS to avoid repeated network calls
jwks_cache = {}

def get_jwks():
    """
    Fetches and caches the JWKS (JSON Web Key Set) from Cognito.

    Returns:
        dict: JWKS containing public keys.
    """
    global jwks_cache
    if not jwks_cache:
        response = requests.get(JWKS_URL)
        jwks_cache = response.json()
    return jwks_cache

def verify_cognito_jwt_token(token: str) -> Optional[dict]:
    """
    Verifies a JWT token from AWS Cognito.

    Args:
        token (str): JWT to verify.

    Returns:
        dict or None: Decoded claims if valid, else None.
    """
    try:
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        if not kid:
            return None

        jwks = get_jwks()
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key:
            return None

        public_key = jwk.construct(key)
        message, encoded_sig = str(token).rsplit(".", 1)
        decoded_sig = base64url_decode(encoded_sig.encode())

        if not public_key.verify(message.encode(), decoded_sig):
            return None

        claims = jwt.get_unverified_claims(token)

        # Use timezone-aware datetime comparison
        if "exp" in claims:
            exp = datetime.fromtimestamp(claims["exp"], timezone.utc)
            if exp < datetime.now(timezone.utc):
                return None

        if claims.get("aud") != APP_CLIENT_ID:
            return None

        return claims

    except Exception as e:
        print("Token verification error:", str(e))
        return None