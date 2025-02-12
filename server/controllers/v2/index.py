from fastapi import HTTPException, status, Request
from ...core.utils.auth import decode_access_token
from ...repositories.activity_repository import *
from ...repositories.user_repository import *
from ...schemas.base_schemas import VerifyEmailResponseSchema


def verify_email(token: str) -> VerifyEmailResponseSchema:
    try:
        payload = decode_access_token(token)
        user = get_user_by_id(payload.get('user_id'))
        
        if user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_is_already_verified")
        
        update_user_profile_data_by_id(user.id, {'verified': True})
        
        create_activity(user_id=user.id, activity_type=ActivityType.EMAIL_VERIFIED)
        
        return VerifyEmailResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))