# Readiness Checklist - Team A2 (Camera Stream)

Tài liệu này đánh giá mức độ sẵn sàng của stack Camera Stream trước khi tích hợp vào hệ thống chung (Plug-a-thon).

## 1. Sẵn sàng Cơ sở dữ liệu (Database Readiness)
- [x] Container `camera-db` đã khởi động thành công.
- [x] Lệnh `pg_isready` trả về trạng thái sẵn sàng.
- [x] Volume `db-data` được gắn đúng để lưu trữ lịch sử detection.

## 2. Sẵn sàng AI Vision Provider (AI Readiness)
- [x] Container `ai-vision-provider` đã load mock logic.
- [x] Endpoint `GET /health` của AI service trả về 200 OK.
- [x] Camera Stream API có thể gọi thành công `POST /detect` sang AI service qua network `team-internal`.

## 3. Xác thực & Bảo mật (Token & Auth)
- [x] Biến môi trường `AUTH_TOKEN` được thiết lập (mặc định: `lab-token`).
- [x] Header `Authorization: Bearer <token>` hoạt động đúng cho các endpoint nghiệp vụ.
- [x] Không có secret/password thật sự bị commit vào git (đã kiểm tra `.env`).

## 4. Cấu hình Port & Network
- [x] Camera Stream API lắng nghe trên port công cộng `8000`.
- [x] AI Service lắng nghe nội bộ trên port `9000`.
- [x] Network `team-internal` cho phép giao tiếp giữa API, DB và AI Provider.
- [x] Sẵn sàng kết nối với `class-net` để nhận request từ Core Business.

## 5. Luồng nghiệp vụ Async (Async Flow & Version)
- [x] `POST /detect` trả về code `202 Accepted` và `detectionId` theo đúng contract.
- [x] Trạng thái ban đầu của detection là `PROCESSING`.
- [x] Version API được thiết lập là `1.0.0` (khớp với `SERVICE_VERSION` trong `.env`).

## 6. Kiểm thử tự động (Contract Testing)
- [x] Postman Collection đã được cập nhật cho các endpoint Camera Stream.
- [x] Chạy thành công Newman test cho luồng: Detect -> Check Status -> List Detections.
- [x] Report XML/HTML đã được sinh ra trong thư mục `reports/`.
