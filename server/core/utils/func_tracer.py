import time
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def func_tracer(func):
    """Universal tracing decorator for FastAPI routes."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.info(f"Function `{func.__name__}` started execution.")

        result = await func(*args, **kwargs)

        execution_time = time.time() - start_time
        logging.info(f"Function `{func.__name__}` finished execution in {execution_time:.4f} seconds.")
        
        return result
    return wrapper