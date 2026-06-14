# Lab 05 Completion Summary

## Ngày hoàn thành: 2026-06-14

Tài liệu này tóm tắt các yêu cầu của Lab 05 và xác nhận trạng thái hoàn thành của từng phần.

---

## ✅ Yêu cầu hoàn thành

### 1. Docker Compose Stack
- [x] File `docker-compose.yml` với 3 services (API, Database, AI)
- [x] Network `team-internal` được định nghĩa
- [x] Volume `db-data` cho PostgreSQL
- [x] Healthcheck cho mỗi service
- [x] Environment variables từ `.env`
- [x] Depends_on với service_healthy condition

**File:** [docker-compose.yml](../docker-compose.yml)

### 2. Dockerfile & Images
- [x] Multi-stage build cho API
- [x] Non-root user `appuser`
- [x] Healthcheck endpoint
- [x] Environment variables
- [x] `.dockerignore` loại trừ không cần thiết

**File:** [Dockerfile](../Dockerfile)  
**File:** [.dockerignore](../.dockerignore)

### 3. Configuration Management
- [x] `.env.example` với tất cả biến cần thiết
- [x] Không commit secret thật
- [x] Hỗ trợ môi trường local
- [x] Đầy đủ các biến: `APP_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `AUTH_TOKEN`, `SERVICE_VERSION`, `ENV`

**File:** [.env.example](../.env.example)

### 4. API Service
- [x] FastAPI với các endpoints:
  - `GET /health` – kiểm tra trạng thái
  - `POST /readings` – tạo bản ghi cảm biến (yêu cầu token)
  - `GET /readings/latest` – lấy readings gần nhất
  - `GET /readings/{reading_id}` – lấy chi tiết reading
- [x] Bearer token authentication
- [x] Validation & error handling
- [x] Problem+JSON error response

**File:** [src/iot_app/main.py](../src/iot_app/main.py)

### 5. AI Service
- [x] Mock AI service với endpoints:
  - `GET /health` – kiểm tra trạng thái
  - `POST /predict` – trả kết quả predictions
- [x] HTTP server chạy trên port 9000
- [x] Sẵn sàng thay bằng YOLOv8 hoặc model khác

**File:** [src/ai_service/main.py](../src/ai_service/main.py)

### 6. Documentation

#### 6.1 README.md
- [x] Ý tưởng & mục tiêu Lab 05
- [x] Cấu trúc repo
- [x] Hướng dẫn chuẩn bị môi trường
- [x] Cách chạy API local
- [x] Chạy stack với Docker Compose
- [x] Readiness checklist
- [x] Các lệnh Makefile
- [x] Điều kiện hoàn thành
- [x] Rubric đánh giá

**File:** [README.md](../README.md)

#### 6.2 RUN_COMPOSE.md
- [x] Yêu cầu tiên quyết (Docker, Node.js)
- [x] Bước clone repo
- [x] Bước cài dependencies
- [x] Build & chạy Docker Compose
- [x] Kiểm tra health của từng service
- [x] Chạy Newman tests
- [x] Tắt stack
- [x] Lệnh nhanh với Makefile
- [x] Mẹo gỡ lỗi
- [x] Kiểm tra chi tiết từng service
- [x] Xem log
- [x] Cấu trúc thư mục tham khảo
- [x] Ghi chú quan trọng

**File:** [RUN_COMPOSE.md](../RUN_COMPOSE.md)

#### 6.3 Readiness Checklist
- [x] 6 tiêu chí kiểm tra sẵn sàng
  1. Database ready
  2. AI service ready
  3. API ready
  4. Environment variables
  5. Network & ports
  6. Image tags & registry
- [x] Lệnh kiểm tra chi tiết cho mỗi tiêu chí
- [x] Bảng trạng thái
- [x] Phần ghi chú vấn đề

**File:** [checklists/readiness-checklist.md](../checklists/readiness-checklist.md)

### 7. OpenAPI Contract
- [x] Spec 3.1.0 đầy đủ cho API
- [x] Các endpoints được định nghĩa
- [x] Request/Response schemas
- [x] Error handling (401, 422, 429)
- [x] Security schemes (Bearer token)
- [x] Examples

**File:** [contracts/iot-ingestion.openapi.yaml](../contracts/iot-ingestion.openapi.yaml)

### 8. Postman Collection & Environment
- [x] Postman collection với 14 test cases:
  - System tests (Health check)
  - Sensor readings (valid, boundary, error cases)
  - Error cases (missing token, invalid payload)
- [x] Postman environment với variables
- [x] Tất cả requests được setup với token

**File:** [postman/collections/FIT4110_lab05.postman_collection.json](../postman/collections/FIT4110_lab05.postman_collection.json)  
**File:** [postman/environments/FIT4110_lab05_local.postman_environment.json](../postman/environments/FIT4110_lab05_local.postman_environment.json)

### 9. Build & Test Automation
- [x] Makefile với các lệnh:
  - `make install` – cài dependencies
  - `make lint` – lint OpenAPI
  - `make build` – build Docker image
  - `make run` – chạy container standalone
  - `make compose-up` – start stack
  - `make compose-down` – stop stack
  - `make logs` – xem logs
  - `make test-compose` – run Newman tests
- [x] package.json với npm scripts

**File:** [Makefile](../Makefile)  
**File:** [package.json](../package.json)

### 10. Reports & Evidence
- [x] Thư mục `reports/` với README
- [x] Hướng dẫn sinh Newman reports
- [x] Template cho evidence capture
- [x] Hướng dẫn tập hợp logs

**File:** [reports/README.md](../reports/README.md)

### 11. Dependencies
- [x] requirements.txt với FastAPI, Uvicorn, Pydantic, requests
- [x] package.json với Newman, Prism, Spectral

**File:** [requirements.txt](../requirements.txt)  
**File:** [package.json](../package.json)

---

## 📋 Checklist Hoàn Thành

Để tuyên bố stack sẵn sàng (ready), hãy kiểm tra:

- [ ] `docker compose up -d --build` chạy thành công
- [ ] Tất cả 3 container up và healthy
- [ ] `curl http://localhost:8000/health` trả 200
- [ ] `curl http://localhost:9000/health` trả 200
- [ ] `docker exec fit4110-db-lab05 pg_isready` trả 0
- [ ] POST `/readings` trả 201 với token hợp lệ
- [ ] GET `/readings/latest` trả 200 với danh sách
- [ ] `npm run test:compose` pass (hoặc import collection vào Postman)
- [ ] Tất cả file documentation đầy đủ
- [ ] Không có secret hardcode trong code
- [ ] `.env.example` có tất cả biến cần thiết

---

## 🚀 Bước tiếp theo

### Chạy stack

```bash
# Chuẩn bị
cp .env.example .env
npm install

# Build & chạy
docker compose up -d --build

# Kiểm tra
docker compose ps
curl http://localhost:8000/health

# Test
npm run test:compose
```

### Dừng stack

```bash
docker compose down
# Hoặc xóa volume DB
docker compose down -v
```

### Nộp bài

Cần nộp:
1. Tất cả source code (src/, contracts/, postman/)
2. Configuration files (docker-compose.yml, Dockerfile, .env.example, .dockerignore)
3. Documentation (README.md, RUN_COMPOSE.md, checklists/)
4. Test reports (reports/*.html, reports/*.xml)
5. Readiness checklist đã check mark

---

## 📝 Ghi chú

**Những gì có thể cải thiện tiếp theo:**

1. Tích hợp thực tế database (tạo schema, lưu dữ liệu)
2. Thay AI service mock bằng YOLOv8 hoặc model thực
3. Thêm CI/CD pipeline (GitHub Actions)
4. Thêm security (rate limiting, request validation)
5. Tối ưu image size (slim images, multi-stage build)

---

## 📚 Tham khảo

- [Lab 05 README](../README.md) – Tài liệu chính
- [Run Compose Guide](../RUN_COMPOSE.md) – Hướng dẫn chạy chi tiết
- [Readiness Checklist](../checklists/readiness-checklist.md) – 6 tiêu chí kiểm tra
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Postman Docs](https://learning.postman.com/)
