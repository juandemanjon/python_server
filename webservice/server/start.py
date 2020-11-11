import asyncio
import logging
import os

from argparse import ArgumentParser

import aiohttp_cors

from aiohttp import web

from .http import http_router
from .rpc import rpc_router

logging.basicConfig(level=logging.INFO)

def run(host, port):

    app = web.Application()

    cors = aiohttp_cors.setup(app,
                              defaults={
                                  "*":
                                  aiohttp_cors.ResourceOptions(
                                      allow_credentials=True,
                                      expose_headers="*",
                                      allow_headers="*",
                                  )
                              })

    # RPC must be first and HTTP second
    rpc_router(app)
    http_router(app)

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, host=host, port=port)

def get_args():
    parser = ArgumentParser()

    parser.add_argument("--host",
                        dest="host",
                        required=False,
                        help="The listener hostname (defaulted to 0.0.0.0)")
    parser.add_argument("--port",
                        dest="port",
                        required=False,
                        help="The listener port (defaulted to 8080)")
    parser.set_defaults(host='0.0.0.0', port=8080)
    return parser.parse_args()



if __name__ == '__main__':
    ARGS = get_args()
    run(ARGS.host, ARGS.port)