import time
import logging
from typing import Annotated
from fastapi import Request, Response, Depends
from ...core.utils.auth import get_session_id
from ...schemas.user_schemas.request import UserLoginRequestSchema
from ...schemas.user_schemas.response import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
session_id_dependency = Annotated[TokenData, Depends(get_session_id)]

def trace_function1(func):
    """Decorator to trace function execution with logging."""
    async def wrapper(session_id: session_id_dependency, request: Request):
        start_time = time.time()
        logging.info(f"Function `{func.__name__}` started")

        # Execute function
        result: UserGetProfileDataResponseSchema = await func(session_id, request)

        execution_time = time.time() - start_time
        logging.info(f"Function `{func.__name__}` finished execution in {execution_time:.4f} seconds.")

        return result
    return wrapper

def trace_function2(func):
    """Decorator to trace function execution with logging."""
    async def wrapper(session_id: session_id_dependency):
        start_time = time.time()
        logging.info(f"Function `{func.__name__}` started")

        # Execute function
        result: UserSendVerifyEmailMailResponseSchema = await func(session_id)

        execution_time = time.time() - start_time
        logging.info(f"Function `{func.__name__}` finished execution in {execution_time:.4f} seconds.")

        return result
    return wrapper