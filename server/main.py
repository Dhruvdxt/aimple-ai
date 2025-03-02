from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler

load_dotenv()

from .core.utils.settings import Settings
Settings.get_from_db()
from .config.fastapi_config import app, limiter
# from .middlewares.exception_logging_middleware import ExceptionLoggingMiddleware
from .routers.v1.index import router as v1
from .routers.v2.index import router as v2

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# app.add_middleware(ExceptionLoggingMiddleware)


app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)


app.include_router(v1)
app.include_router(v2)