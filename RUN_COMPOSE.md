# RUN_COMPOSE.md – Hướng dẫn vận hành Camera Stream Stack (Team A2)

Tài liệu này hướng dẫn chạy toàn bộ stack Camera Stream tích hợp AI Vision dành cho Lab 05.

## 1. Chuẩn bị
```bash
# Copy cấu hình môi trường
cp .env.example .env

# Khởi chạy stack với Docker Compose
docker compose up -d --build
```

## 2. Kiểm tra trạng thái sẵn sàng (Readiness)
Sau khi chạy, hãy đợi các container báo `healthy`. Kiểm tra qua:
- **Camera API (Port 8000):** `curl http://localhost:8000/health`
- **AI Vision Provider (Port 9000):** `curl http://localhost:9000/health`
- **Database:** `docker exec -it camera-db pg_isready -U lab05`

## 3. Kiểm thử luồng Async Detection
Do hệ thống chạy theo mô hình Async (202 Accepted), quy trình kiểm thử như sau:

**Bước 1: Gửi yêu cầu phân tích frame**
```bash
curl -X POST http://localhost:8000/detect \
  -H "Authorization: Bearer lab-token" \
  -H "Content-Type: application/json" \
  -d '{
    "cameraId": "CAM-01",
    "frameUrl": "https://campus.local/frame01.jpg",
    "timestamp": "2026-05-13T10:00:00Z",
    "requestId": "REQ-001",
    "analysisType": "PERSON_DETECTION"
  }'
```
*Kết quả mong đợi:* Trả về `202 Accepted` cùng một `detectionId`.

**Bước 2: Kiểm tra trạng thái xử lý** (Sử dụng `detectionId` từ bước 1)
```bash
curl -H "Authorization: Bearer lab-token" http://localhost:8000/detections/<detectionId>
```
*Kết quả mong đợi:* Ban đầu là `PROCESSING`, sau vài giây sẽ chuyển sang `COMPLETED` kèm dữ liệu `boundingBox` và `trackingId` từ AI Provider.

**Bước 3: Xem danh sách các phát hiện**
```bash
curl -H "Authorization: Bearer lab-token" http://localhost:8000/detections
```

## 4. Dọn dẹp
```bash
docker compose down -v
```
