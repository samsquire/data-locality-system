# data-locality-system

DLS is a library and pattern that tries to keep data and processing near together for latency and performance. It's very much early in development.

# Usage

Split up your API request handler into a series of methods with each method being responsible for some API call or processing.

Automatically

* OpenTracing Jaegar wraps all your spans.
* Requests are routed to servers which are favourable
* Requests run in parallel using a threadpool.

Run each DLS service using Gunicorn.

# Example

Run the [all in one jaegar docker image](https://www.jaegertracing.io/docs/1.18/getting-started/) and go to http://localhost:16686/ and filter by service dls to see Jaegar tracing.

To run the example, start the following in separate terminals:

```
export WORKER_HOST=database ; sudo -E $(which gunicorn) -w 1 -k gevent  dls_example:app --bind 0.0.0.0:9006
```
```
export WORKER_HOST=app ; sudo -E $(which gunicorn) -w 1 -k gevent  dls_example:app --bind 0.0.0.0:9005
```

Then run:

```
WORKER_HOST=client python3.8 dls_example.py
```
