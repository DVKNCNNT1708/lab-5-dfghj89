.PHONY: install lint build run compose-up compose-down logs test-compose

# Cài đặt Node dependencies cho Prism/Newman
install:
	npm install

# Kiểm tra tính hợp lệ của OpenAPI Contract
lint:
	npx spectral lint contracts/camera-ai-vision.openapi.yaml

# Build Docker image cho Camera Stream API
build:
	docker build -t fit4110/camera-stream-api:v1.0.0-a2 .

# Chạy thử container API (không dùng compose)
run:
	docker run --rm --name camera-stream-api -p 8000:8000 --env-file .env.example fit4110/camera-stream-api:v1.0.0-a2

# Điều phối với Docker Compose
compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

# Xem logs của toàn bộ hệ thống
logs:
	docker compose logs -f

# Chạy test Newman trên stack Compose
test-compose:
	npm run test:compose
