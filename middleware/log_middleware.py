from fastapi import Request
from utils.logger_utils import logger
import time




async def log_middleware(request: Request, call_next):
    """
    Middleware function that logs information about incoming requests and their processing time.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): The next middleware function in the chain.

    Returns:
        Response: The response object returned by the next middleware function.

    Logs:
        - Information about the incoming request, including the URL path, HTTP method, processing time, and client host.

    """
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start

    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "process_time": process_time,
        "host": request.client.host
    }
    logger.info(log_dict, extra=log_dict)

    return response