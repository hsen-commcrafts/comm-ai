import os
import hmac
import time
import hashlib
import fasttext
from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
#     docs_url=None,     # disables Swagger UI (/docs)
#     redoc_url=None,    # disables ReDoc UI (/redoc)
#     openapi_url=None   # disables OpenAPI schema (/openapi.json)
)
MODEL_PATH = os.getenv("MODEL_PATH")
HMAC_SECRET = os.getenv("HMAC_SECRET")


class FlowBody(BaseModel):
    text: str


def verify_hmac(request: Request):

    signature = request.headers.get("X-Signature")
    timestamp = request.headers.get("X-Timestamp")

    if not signature or not timestamp:
        raise HTTPException(status_code=401, detail="Missing HMAC headers")

    # Optional: block old timestamps (e.g., over 5 minutes)
    try:
        if abs(time.time() - int(timestamp)) > 300:
            raise HTTPException(status_code=401, detail="Request expired")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")

    # Create expected signature from timestamp + static message
    message = f"{timestamp}|flow_request"
    expected_signature = hmac.new(
        HMAC_SECRET.encode(), message.encode(), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")


@app.post("/api/flow", dependencies=[Depends(verify_hmac)])
def flow(flow_body: FlowBody):
    model = fasttext.load_model(MODEL_PATH)
    text = flow_body.text
    label, confidence = model.predict(text)
    return {"label": label[0].replace("__label__", ""), "confidence": confidence[0]}
