import logging
import os

from fastapi import Request
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

SERVICE_NAME = "order-tracker"


def setup_telemetry(app):
    """Export traces, metrics and logs.

    With OTEL_EXPORTER_OTLP_ENDPOINT set (docker compose) they go to the OpenTelemetry
    Collector over OTLP/HTTP; otherwise they are printed to the console.
    """
    use_otlp = bool(os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"))
    span_exporter = OTLPSpanExporter() if use_otlp else ConsoleSpanExporter()
    metric_exporter = OTLPMetricExporter() if use_otlp else ConsoleMetricExporter()
    log_exporter = OTLPLogExporter() if use_otlp else ConsoleLogExporter()
    resource = Resource.create({"service.name": SERVICE_NAME})

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=5_000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(LoggingHandler(level=logging.INFO, logger_provider=logger_provider))

    # http.server.duration histogram carries http.route and http.status_code
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=tracer_provider,
        meter_provider=meter_provider,
        excluded_urls="healthz",
    )

    # The instrumentation's duration histogram has no route label, so count requests
    # ourselves with route + status code. The route is the template (/api/orders/{order_id}),
    # which keeps label cardinality low.
    request_counter = meter_provider.get_meter(SERVICE_NAME).create_counter(
        "http.server.requests",
        unit="{request}",
        description="HTTP requests by method, route and status code",
    )

    @app.middleware("http")
    async def count_requests(request: Request, call_next):
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            return response
        finally:
            route = request.scope.get("route")
            request_counter.add(1, {
                "http.method": request.method,
                "http.route": route.path if route else "unmatched",
                "http.status_code": status,
            })
