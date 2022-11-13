from fastapi import FastAPI,Request
from utils.babel import _,babel,configs
from datetime import timedelta
import time

SUPPORTED_LANGUAGE = ['pt-BR','en','zh']


class Middleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        assert scope["type"] == "http"
        headers = dict(scope["headers"])
        lang = str(headers.get(b'accept-language',b''), 'UTF-8').split(',')[0]
        headers[b'accept-language'] = bytes(configs.BABEL_DEFAULT_LOCALE if lang not in SUPPORTED_LANGUAGE else lang,'UTF-8')
        scope["headers"] = [(k, v) for k, v in headers.items()]
        await self.app(scope, receive, send)

def add_middlewares(app:FastAPI):
    app.add_middleware(Middleware)
    
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Process-Time-Format"] = str(timedelta(seconds=process_time))
        # logger.debug("/api/log_now starts")
        # logger.info("I'm logging")
        # logger.warning("some warnings")
        return response