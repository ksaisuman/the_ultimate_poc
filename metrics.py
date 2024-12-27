from prometheus_client import Counter, Histogram
from prometheus_client import multiprocess
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
from django.http import HttpResponse

# Prometheus metrics
REQUEST_COUNT = Counter(
    "app_request_count", "Total HTTP requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "HTTP request latency", ["method", "endpoint"]
)


# Expose metrics.
def metrics(request):
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
