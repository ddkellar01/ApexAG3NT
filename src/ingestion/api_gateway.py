from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import os

app = FastAPI(title="Apex Webhook Gateway")

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "dev_secret").encode()

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """Verifies HMAC SHA-256 signatures from GitHub webhooks."""
    if not signature_header:
        return False
    hash_object = hmac.new(WEBHOOK_SECRET, msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)

@app.post("/webhooks/github")
async def receive_github_webhook(request: Request):
    """Entrypoint for automated CI/CD pipeline triggers."""
    signature = request.headers.get("x-hub-signature-256", "")
    body = await request.body()
    
    if not verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    event_type = request.headers.get("x-github-event", "unknown")
    
    # In a real app, this drops the payload into the StreamListener queue
    return {"status": "accepted", "event": event_type, "action": payload.get("action")}
