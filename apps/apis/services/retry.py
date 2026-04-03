import logging
from functools import wraps
from typing import Callable, TypeVar

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from apps.apis.config import RETRY_MAX_ATTEMPTS
from apps.apis.exceptions import ProviderUnavailable


logger = logging.getLogger(__name__)


T = TypeVar("T")


def with_retry(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    @retry(
        stop=stop_after_attempt(RETRY_MAX_ATTEMPTS),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(ProviderUnavailable),
        reraise=True,
    )
    def wrapper(*args, **kwargs):
        logger.info(f"Attempting {func.__name__}", extra={"function": func.__name__})
        try:
            return func(*args, **kwargs)
        except ProviderUnavailable as e:
            logger.warning(f"Retry needed for {func.__name__}: {e}")
            raise

    return wrapper
