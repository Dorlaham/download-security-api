# Download Security System – Backend (FastAPI)

## 🧠 Overview

This is the backend component of the Chrome download security system, built with FastAPI.  
It serves as the API layer for verifying downloaded file types, logging actions, and managing system configurations.

## 🔗 Endpoints

### `POST /api/verify-file`
Verifies a file's MIME type using its magic bytes and determines if the file should be allowed or blocked.

Request payload:
```json
{
  "filename": "example.exe",
  "url": "https://example.com/file",
  "mime": "application/octet-stream",
  "magic_bytes": "BASE64_ENCODED_BYTES"
}
```

Response:
```json
{
  "allow": false
}
```

### `GET /api/logs`
Returns download logs (paginated).  
Requires valid Cognito JWT and appropriate group permissions.

### `GET /api/config/blocked-types`
Returns a list of currently blocked MIME types.

### `PUT /api/config/blocked-types`
Updates the list of blocked MIME types (admin-only).

---

## 🔐 Authentication

- All protected endpoints use **JWT tokens issued by AWS Cognito**
- Tokens are verified manually via JOSE & JWKS:
  - Signature
  - `exp` (expiry)
  - `aud` (client ID match)
  - `cognito:groups` for access control

Authorization is enforced via FastAPI middleware.

---

## 🧾 Logging Architecture

- Logs are generated for every file verification request.
- Logs are serialized and sent to **AWS SQS** via a decorator.
- A separate **Lambda function** consumes the queue and writes logs to **DynamoDB**.

---

## 🛠 Tech Stack

- FastAPI
- Python 3.11+
- python-magic
- boto3
- jose (JWT handling)
- DynamoDB (log storage)
- SQS (log queue)

---

## 🧪 Running Locally

```sh
# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload
```

---

## 📌 Notes

- CORS is configured via regular expression to allow:
  - The production portal domain (`https://dorlaham-secure.com`)
  - Chrome extension origin (`chrome-extension://*`)
  - Local development (`http://localhost:8080`)
- File type detection is based on magic bytes using `libmagic` (via `python-magic`) — not just filename or extension.
- Every file verification request is logged and traceable through the logging pipeline (SQS + Lambda + DynamoDB).
