"""
Integration with Arize Phoenix for experiment telemetry via OpenTelemetry.
Falls back gracefully if Phoenix is unavailable.
"""

import os
import contextlib
from typing import Optional

# Environment config
PHOENIX_ENDPOINT = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006")
PHOENIX_PROJECT = os.getenv("PHOENIX_PROJECT_NAME", "autoresearch-lab")
OTLP_ENDPOINT = f"{PHOENIX_ENDPOINT}/v1/traces"

_tracer = None


def setup_tracer():
    """Initialize OpenTelemetry tracer pointing at Arize Phoenix. Fails silently."""
    global _tracer
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource

        resource = Resource.create({
            "service.name": PHOENIX_PROJECT,
        })
        provider = TracerProvider(resource=resource)
        exporter = OTLPSpanExporter(endpoint=OTLP_ENDPOINT)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer(PHOENIX_PROJECT)
        print(f"Phoenix tracing enabled → {OTLP_ENDPOINT}")
    except Exception as e:
        print(f"Phoenix tracing unavailable (continuing without it): {e}")
        _tracer = None


@contextlib.contextmanager
def trace_span(span_name: str, attributes: Optional[dict] = None):
    """Context manager that creates a named span with optional attributes."""
    if _tracer is None:
        yield None
        return
    try:
        with _tracer.start_as_current_span(span_name) as span:
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, value)
            yield span
    except Exception:
        yield None


def log_experiment_step(step_name: str, data: dict):
    """Log a discrete experiment step as a span with data as attributes."""
    if _tracer is None:
        return
    try:
        with _tracer.start_as_current_span(step_name) as span:
            for key, value in data.items():
                span.set_attribute(str(key), str(value))
    except Exception:
        pass
