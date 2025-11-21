import time

from fastapi import FastAPI
from httpcore import Request
from prometheus_client import start_http_server

from app.api.v1.api import api_router
from app.metrics import REQUEST_COUNT, REQUEST_LATENCY

app = FastAPI(title="Hotels Management")
app.include_router(api_router)


@app.on_event("startup")
def startup_event():
    try:
        start_http_server(8081)
        print("Prometheus metrics server started on port 8081")
    except Exception as e:
        print(f"Error starting metrics server: {e}")


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    # 1. Lấy label 'http_method'
    method = request.method

    # 2. Lấy label 'http_handler' (quan trọng!)
    # LƯU Ý: Phải dùng template path (ví dụ /users/{id}) thay vì path thật (/users/123)
    # để tránh lỗi "Label Explosion" (Trang 3 guideline)
    handler = "unknown"

    # Bắt đầu đo thời gian
    start_time = time.time()

    try:
        response = await call_next(request)

        # Lấy path template từ router nếu có
        route = request.scope.get("route")
        if route:
            handler = route.path
        else:
            # Fallback nếu không match được route
            handler = request.url.path

        # 3. Lấy label 'http_status_code'
        status_code = str(response.status_code)

        # --- GHI NHẬN METRICS ---
        # Ghi nhận số lượng request
        REQUEST_COUNT.labels(
            http_method=method,
            http_status_code=status_code,
            http_handler=handler
        ).inc()

        # Ghi nhận thời gian xử lý
        process_time = time.time() - start_time
        REQUEST_LATENCY.labels(
            http_method=method,
            http_status_code=status_code,
            http_handler=handler
        ).observe(process_time)

        return response

    except Exception as e:
        # Trường hợp lỗi 500 (Unhandled Exception)
        # Vẫn phải ghi metrics để biết service đang lỗi
        process_time = time.time() - start_time
        REQUEST_COUNT.labels(
            http_method=method,
            http_status_code="500",
            http_handler=handler
        ).inc()
        REQUEST_LATENCY.labels(
            http_method=method,
            http_status_code="500",
            http_handler=handler
        ).observe(process_time)
        raise e