from prometheus_client import Counter, Histogram

# 1. Metrics đếm số lượng request (Traffic)
# Tên metric chuẩn: http_server_handled_total
# Labels bắt buộc: http_method, http_status_code, http_handler
REQUEST_COUNT = Counter(
    'http_server_handled_total',
    'Count of inbound HTTP requests handled by the service',
    ['http_method', 'http_status_code', 'http_handler']
)

# 2. Metrics đo độ trễ (Latency)
# Tên metric chuẩn: http_server_handling_seconds
# (Prometheus sẽ tự thêm hậu tố _bucket, _sum, _count)
REQUEST_LATENCY = Histogram(
    'http_server_handling_seconds',
    'Latency histogram for inbound HTTP',
    ['http_method', 'http_status_code', 'http_handler']
)