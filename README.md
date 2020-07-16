# data-locality-system

DLS is a library and pattern that tries to keep data and processing near together for latency and performance.

# Usage

Split up your API request handler into a series of methods with each method being responsible for some API call or processing.

Automatically

* OpenTracing wraps all your spans
* Requests are routed to servers which are favourable
* Requests run in parallel using threads.

Run each DLS service using Gunicorn.

# Example

To run the example, start the following in separate terminals:

```
export WORKER_HOST=database ; sudo -E $(which gunicorn) -w 1 -k gevent  dls_example:app --bind 0.0.0.0:9006
export WORKER_HOST=app ; sudo -E $(which gunicorn) -w 1 -k gevent  dls_example:app --bind 0.0.0.0:9005
```

Then run:

```
WORKER_HOST=client python3.8 dls_example.py
```
