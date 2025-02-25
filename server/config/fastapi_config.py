from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address

app = FastAPI(
    title="Aimple AI",
    version="1.0.0",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    }
)

limiter = Limiter(key_func=get_remote_address)