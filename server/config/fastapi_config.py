from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter
from slowapi.util import get_remote_address

app = FastAPI(
    title="Aimple AI",
    version="1.0.0",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    }
)

app.add_security_scheme = {
    "user_auth": {
        "type": "oauth2",
        "flows": {
            "password": {
                "tokenUrl": "api/v1/user/login",
                "scopes": {}
            }
       }
    },
    "admin_auth": {
        "type": "oauth2",
        "flows": {
            "password": {
                "tokenUrl": "api/v1/admin/login",
                "scopes": {}
            }
       }
    }
}

user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/user/login",
    scheme_name="user_auth",
    auto_error=True
)

admin_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/admin/login",
    scheme_name="admin_auth",
    auto_error=True
)

limiter = Limiter(key_func=get_remote_address)