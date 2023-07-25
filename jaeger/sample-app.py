import time
import logging
from jaeger_client import Config

def init_tracer():
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': '10.43.61.111',
                'reporting_port': 14250,  # Replace with your Jaeger collector service address
            },
            'logging': True,
        },
        service_name='test-service',
    )

    return config.initialize_tracer()

def main():
    tracer = init_tracer()

    with tracer.start_span('TestSpan') as span:
        span.log_kv({'event': 'test-message', 'value': 42})

        # Simulate some work
        time.sleep(2)

    tracer.close()

if __name__ == "__main__":
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    main()