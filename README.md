# data-locality-system

DLS is a library and pattern that tries to keep data and processing near together for latency and performance.

# Usage

Split up your API request handler into a series of methods with each method being responsible for some API call or processing.

Automatically

* OpenTracing wraps all your spans
* Requests are routed to servers which are favourable
* Requests run in parallel using threads.

# Usage

Run each DLS service using Gunicorn.
