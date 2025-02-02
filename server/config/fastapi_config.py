from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

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
                "tokenUrl": "/user/login",
                "scopes": {}
            }
       }
    },
    "admin_auth": {
        "type": "oauth2",
        "flows": {
            "password": {
                "tokenUrl": "/admin/login",
                "scopes": {}
            }
       }
    }
}

user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="user/login",
    scheme_name="user_auth",
    auto_error=True
)

admin_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="admin/login",
    scheme_name="admin_auth",
    auto_error=True
)