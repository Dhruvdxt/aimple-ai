from fastapi import APIRouter
from ...controllers.v2.index import *
from ...schemas.base_schemas import VerifyEmailResponseSchema


router = APIRouter(prefix="/api/v2")


@router.get("/verify_email", response_model=VerifyEmailResponseSchema,  tags=['V2'])
async def _verify_email(token: str):
    return verify_email(token)
    