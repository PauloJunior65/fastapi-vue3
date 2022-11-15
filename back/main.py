from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from utils.babel import _,babel
from utils.middleware import add_middlewares
from utils.logging import create_log
from utils.database import get_db
from utils.cache import get_cache,RedisCache
import pickle


from routers import users



app = FastAPI()
babel.init_app(app)
add_middlewares(app)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(users.router)

# init our logger
log = create_log(__name__)

@app.get("/log_now")
async def log_now(db: Session = Depends(get_db),cache: RedisCache = Depends(get_cache)):
    con = cache.get('TESTE')
    if con is None:
        con = db.execute("SELECT * FROM `auth_user`;").fetchall()
        cache.set('TESTE',con)
    return con
    log.debug('debug message')
    log.info('info message')
    log.warning('warn message')
    log.error('error message')
    log.critical('critical message')
    
    return {"result": "OK"}

