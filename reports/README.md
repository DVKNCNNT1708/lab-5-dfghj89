# Reports Directory

Thư mục này chứa các báo cáo test và bằng chứng thực thi stack Docker Compose của Lab 05.

## Nội dung

### Test Reports
- `newman-lab05-compose.xml` – XML report từ Newman test
- `newman-lab05-compose.html` – HTML report từ Newman test (dễ xem)

### Evidence
- `docker-compose-ps.txt` – Screenshot/output của `docker compose ps`
- `health-checks.txt` – Output của kiểm tra `/health` từ mỗi service
- `network-test.txt` – Output của kiểm tra network và hostname resolution
- `logs/` – Log files từ các service

## Cách sinh các báo cáo

### 1. Run Newman test

```bash
npm run test:compose
```

Output sẽ tạo ra `newman-lab05-compose.xml` và `newman-lab05-compose.html` trong thư mục này.

### 2. Capture evidence

```bash
# Docker Compose status
docker compose ps > reports/docker-compose-ps.txt

# Health checks
echo "=== API Health ===" >> reports/health-checks.txt
curl http://localhost:8000/health >> reports/health-checks.txt

echo "=== AI Health ===" >> reports/health-checks.txt
curl http://localhost:9000/health >> reports/health-checks.txt

echo "=== DB Ready ===" >> reports/health-checks.txt
docker exec -it fit4110-db-lab05 pg_isready -U lab05 >> reports/health-checks.txt

# Network test
docker compose exec api curl http://ai-service:9000/health > reports/network-test.txt

# Logs
mkdir -p reports/logs
docker compose logs > reports/logs/compose-logs.txt
```

### 3. Nộp bài

Tất cả các file trong thư mục này cần được nộp cùng với code để chứng minh stack hoạt động đúng.
