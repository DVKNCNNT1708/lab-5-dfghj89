import os
import uuid
import asyncio
import httpx
from datetime import datetime, timezone
from typing import List, Optional, Dict
from fastapi import FastAPI, BackgroundTasks, HTTPException, status, Header, Depends
from pydantic import BaseModel, Field

# Configuration
SERVICE_NAME = os.getenv("SERVICE_NAME", "camera-stream-service")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "local-dev-token")
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://ai-service:9000")

app = FastAPI(
    title="Camera Stream API",
    version=SERVICE_VERSION,
    description="Service for camera frame analysis and tracking (Lab 05).",
)

# In-memory storage (In Lab 05, we simulate DB usage)
DETECTIONS_DB: Dict[str, dict] = {}

class AnalysisType(str):
    PERSON_DETECTION = "PERSON_DETECTION"
    VEHICLE_DETECTION = "VEHICLE_DETECTION"
    UNKNOWN = "UNKNOWN"

class DetectRequest(BaseModel):
    cameraId: str
    frameUrl: str
    timestamp: str
    requestId: str
    analysisType: str

class DetectionResponse(BaseModel):
    detectionId: str
    status: str

def verify_token(authorization: str = Header(None)):
    if not authorization or authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}

async def notify_ai_and_update(detection_id: str, payload: DetectRequest):
    """
    Simulates calling the AI Provider and updating the local DB.
    """
    try:
        async with httpx.AsyncClient() as client:
            # Step 1: Forward to AI Service
            response = await client.post(
                f"{AI_SERVICE_URL}/detect",
                json=payload.model_dump(),
                timeout=5.0
            )
            if response.status_code == 202:
                ai_data = response.json()
                # Step 2: Update local status (In real app, we'd wait for AI webhook)
                DETECTIONS_DB[detection_id]["status"] = "PROCESSING"
                DETECTIONS_DB[detection_id]["ai_ref"] = ai_data.get("detectionId")
            else:
                DETECTIONS_DB[detection_id]["status"] = "FAILED"
    except Exception as e:
        print(f"Error calling AI service: {e}")
        DETECTIONS_DB[detection_id]["status"] = "FAILED"

@app.post("/detect", status_code=status.HTTP_202_ACCEPTED, response_model=DetectionResponse, dependencies=[Depends(verify_token)])
async def create_detection(payload: DetectRequest, background_tasks: BackgroundTasks):
    detection_id = str(uuid.uuid4())

    # Save initial state to "DB"
    DETECTIONS_DB[detection_id] = {
        "detectionId": detection_id,
        "status": "ACCEPTED",
        "details": payload.model_dump()
    }

    # Trigger async processing
    background_tasks.add_task(notify_ai_and_update, detection_id, payload)

    return {"detectionId": detection_id, "status": "PROCESSING"}

@app.get("/detections", dependencies=[Depends(verify_token)])
def list_detections(cursor: Optional[str] = None, limit: int = 20):
    items = list(DETECTIONS_DB.values())
    return {
        "items": items[:limit],
        "nextCursor": None,
        "hasMore": False
    }

@app.get("/detections/{detection_id}", dependencies=[Depends(verify_token)])
def get_detection(detection_id: str):
    if detection_id not in DETECTIONS_DB:
        raise HTTPException(status_code=404, detail="Detection not found")
    return DETECTIONS_DB[detection_id]
