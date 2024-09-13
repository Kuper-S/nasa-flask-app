from prometheus_flask_exporter import Counter, Gauge, PrometheusMetrics

def setup_metrics(app):
    # Initialize Prometheus metrics
    metrics = PrometheusMetrics(app)

    # Define a counter to track requests by method and endpoint
    request_counter = Counter('app_requests_total', 'Total number of requests', ['method', 'endpoint'])

    # Gauge to track number of in-progress database queries
    db_query_gauge = Gauge('db_queries_in_progress', 'Number of database queries in progress')

    return metrics, request_counter, db_query_gauge