import uvicorn
import logging
from utils.config import settings
FORMAT: str = "%(levelprefix)s %(name)s | %(asctime)s | %(message)s"

def create_log(name: str = 'simple_example'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = uvicorn.logging.DefaultFormatter(FORMAT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
