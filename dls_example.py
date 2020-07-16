import sys
import os
import time
from pprint import pprint
import networkx as nx
from networkx.algorithms.dag import topological_sort
from component_scheduler.scheduler import parallelise_components
import psycopg2
import redis
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from threading import Thread
from flask import Flask, request
import requests
import pickle
from opentracing.propagation import Format
import json
from dls.dls_api import app, register_resource, register_host, register_span, initialize_group, run_group, configure_tracer, initialize_host
from jaeger_client import Config

hostname = os.environ["WORKER_HOST"]



configure_tracer(Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='dls',
        validate=True
))

def connect_to_database(resources, host):
    resources.conn = psycopg2.connect("dbname='forum' user='forum' host='" + host + "' password='forum'")
    print(resources.conn)

def connect_to_redis(resources, host):
    resources.r = redis.Redis(host=host, port=6379, db=0)
    print(resources.r)


register_resource("communities database", connect_to_database)
register_resource("redis cache", connect_to_redis)

register_host(name="app", port=9005, host="localhost", has=[])
register_host(name="database", port=9006, host="localhost", has=["communities database", "redis cache"])

def get_community(r, o):
    print("Getting community query from database")
    o.community = 6


def get_exact_posts(r, o):
    print("Getting exact posts from database")
    o.exact_posts = ["An exact post"]


def get_partial_posts(r, o):
    print("Getting partial posts from database")
    o.partial_posts = ["A partial search result"]


def combine_work(r, o):
    print("Combining work")
    o.combine = o.partial_posts + o.exact_posts


def get_parent_communities(r, o):
    o.parent_posts = ["one"]

register_span("get communities",
    "app.get community",
    [],
    get_community)
register_span("get communities",
    "database.get exact posts",
    ["app.get community", "@communities database"],
    get_exact_posts)
register_span("get communities",
    "database.get partial posts",
    ["app.get community", "@communities database"],
    get_partial_posts)
register_span("get communities",
    "app.combine work",
    ["database.get exact posts", "database.get partial posts"],
    combine_work)
register_span("get communities",
    "get parent communities",
    ["@communities database",
    "app.combine work"],
    get_parent_communities)

spans = initialize_group("get communities")

initialize_host(spans, hostname)

if __name__ == "__main__":
    t0 = time.time()
    outputs = run_group(False, spans, "client", "get communities")
    print(outputs.exact_posts)
    print(outputs.partial_posts)
    print(outputs.community)
    print(outputs.combine)
    print(outputs.parent_posts)
    t1 = time.time()
    print((t1-t0)*1000)
