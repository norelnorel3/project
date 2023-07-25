import time
import requests
from jaeger_client import Config
from opentracing_instrumentation.client_hooks import install_all_patches

def make_request():
    url = "https://api.github.com/"
    response = requests.get(url)
    return response.status_code

# Replace these values with your Jaeger deployment details
JAEGER_HOST = "localhost"  # For example, "jaeger-collector.my-namespace.svc.cluster.local"
JAEGER_PORT = 32643  # Use the appropriate port based on gRPC or HTTP/JSON
SERVICE_NAME = "jaeger-collector"  # Set this to your service or application name

# Create a Jaeger configuration
config = Config(
    config={
        "sampler": {"type": "const", "param": 1},
        "logging": True,
    },
    service_name=SERVICE_NAME,
)

# Install client-side instrumentation hooks
install_all_patches()

# Create a Tracer instance from the configuration
tracer = config.initialize_tracer()

# Function to trace
def trace_function():
    # Start a span
    with tracer.start_span("main") as span:
        span.set_tag("example.tag", "example-value")
        try:
            # Simulate some work
            time.sleep(1)
            # Call the function that makes the HTTP request
            status_code = make_request()
            # Set the HTTP status code as a tag
            span.set_tag("http.status_code", status_code)
        except Exception as e:
            # Log any exceptions that occur during the trace
            span.set_tag("error", True)
            span.log_kv({"event": "error", "message": str(e)})
        finally:
            # Finish the span
            span.finish()

if __name__ == "__main__":
    # Trace the function
    trace_function()

    # Close the tracer
    tracer.close()