from aiohttp import web
import json

async def root_handle(request):
    response_obj = { 'status' : 'success' }
    return web.Response(text=json.dumps(response_obj))


def http_router(app):
  app.router.add_get('/', root_handle)