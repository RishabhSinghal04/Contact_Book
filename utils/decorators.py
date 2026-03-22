import functools
import time

from typing import Callable, TypeVar, ParamSpec

from utils.logger import get_logger

logger = get_logger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def log_execution(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to log function execution."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> R:
        logger.debug(f"Executing {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Completed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper


def measure_time(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to measure execution time."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> R:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"{func.__name__} took {duration:.4f} seconds")
        return result

    return wrapper


def handle_exception(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator for centralized exception handling."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}")
            raise

    return wrapper
