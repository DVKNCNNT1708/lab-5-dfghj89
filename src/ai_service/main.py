import uuid
import asyncio
from datetime import datetime, timezone
from typing import List, Optional, Dict
from fastapi import FastAPI, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, Field

SERVICE_NAME = "ai-vision-service"
SERVICE_VERSION = "1.0.0"

app = FastAPI(
    title="Camera Stream - AI Vision Service",
    version=SERVICE_VERSION,
    description="Mock AI Vision service for object detection in camera frames.",
)

# In-memory storage for detections
DETECTIONS_DB: Dict[str, dict] = {}

class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int

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

class DetectionResult(BaseModel):
    detectionId: str
    status: str
    detectionType: Optional[str] = None
    confidence: Optional[float] = None
    boundingBox: Optional[BoundingBox] = None
    trackingId: Optional[str] = None

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}

async def process_detection(detection_id: str, analysis_type: str):
    # Simulate processing time
    await asyncio.sleep(2)

    # Mock result generation
    if detection_id in DETECTIONS_DB:
        DETECTIONS_DB[detection_id].update({
            "status": "COMPLETED",
            "detectionType": "PERSON" if analysis_type == "PERSON_DETECTION" else "VEHICLE",
            "confidence": 0.98,
            "boundingBox": {"x": 150, "y": 100, "width": 200, "height": 300},
            "trackingId": f"TRACK-{uuid.uuid4().hex[:8].upper()}"
        })
        # Note: In a real scenario, we would trigger the webhook here
        print(f"Detection {detection_id} completed via background task.")

@app.post("/detect", status_code=status.HTTP_202_ACCEPTED, response_model=DetectionResponse)
async def detect(payload: DetectRequest, background_tasks: BackgroundTasks):
    detection_id = str(uuid.uuid4())

    DETECTIONS_DB[detection_id] = {
        "detectionId": detection_id,
        "status": "PROCESSING",
        "cameraId": payload.cameraId,
        "analysisType": payload.analysisType,
        "timestamp": payload.timestamp
    }

    background_tasks.add_task(process_detection, detection_id, payload.analysisType)

    return {"detectionId": detection_id, "status": "PROCESSING"}

@app.get("/detections")
def list_detections(cursor: Optional[str] = None, limit: int = 20):
    items = list(DETECTIONS_DB.values())
    # Simple pagination logic
    return {
        "items": items[:limit],
        "nextCursor": None,
        "hasMore": False
    }

@app.get("/detections/{detection_id}", response_model=DetectionResult)
def get_detection(detection_id: str):
    if detection_id not in DETECTIONS_DB:
        raise HTTPException(status_code=404, detail="Detection not found")
    return DETECTIONS_DB[detection_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
