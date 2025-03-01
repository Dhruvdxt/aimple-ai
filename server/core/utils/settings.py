from fastapi import status, HTTPException
from ...repositories.settings_repository import *


class Settings():
    SESSION_EXPIRE_MINUTES = 10
    OTP_VALIDATION_TIME = 120
    LOGIN_RATE_LIMIT = "10/minute"
    FAILED_ATTEMPT_LIMIT = 5
    BLOCK_DURATION = 7200
    ATTEMPT_RESET_TIME = 300
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    @classmethod
    def get_from_db(cls):
        try:
            settings = get_all_settings()
            for data in settings:
                if data.name == "SESSION_EXPIRE_MINUTES":
                    cls.SESSION_EXPIRE_MINUTES = int(data.value)
                elif data.name == "OTP_VALIDATION_TIME":
                    cls.OTP_VALIDATION_TIME = int(data.value)
                elif data.name == "LOGIN_RATE_LIMIT":
                    cls.LOGIN_RATE_LIMIT = data.value
                elif data.name == "FAILED_ATTEMPT_LIMIT":
                    cls.FAILED_ATTEMPT_LIMIT = int(data.value)
                elif data.name == "BLOCK_DURATION":
                    cls.BLOCK_DURATION = int(data.value)
                elif data.name == "ATTEMPT_RESET_TIME":
                    cls.ATTEMPT_RESET_TIME = int(data.value)
                elif data.name == "ACCESS_TOKEN_EXPIRE_MINUTES":
                    cls.ACCESS_TOKEN_EXPIRE_MINUTES = int(data.value)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    # def update(cls, update_data: dict):
    #     try:
    #         for k, v in update_data.items():
    #             cls.k = v
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    