from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from utils.babel import _,babel
from utils.middleware import add_middlewares

from routers import users

# from utils.database import engine
# import models
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()
babel.init_app(app)
add_middlewares(app)
app.mount("/static", StaticFiles(directory="static"), name="static")




app.include_router(users.router)

