from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler

load_dotenv()

from .config.fastapi_config import app, limiter
from .routers.v1.index import router as v1
from .routers.v2.index import router as v2


# def test_function():
#     try:
#         ServiceFactory().get(service_type=ServiceType.MAIL_SERVICE).get(mail_type=MailType.VERIFY_EMAIL).send(recipient="dhruv@aimple.ai", provider=MProviderType.SES, verification_link="https://google.com")
#         print("Mail sent")
#         print("Check out your inbox")
#     except Exception as e:
#         raise 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)


app.include_router(v1)
app.include_router(v2)