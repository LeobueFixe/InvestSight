import random
import time
from functools import wraps
from apps.apis.services.logging import get_logger
from apps.apis.settings import settings

logger = get_logger("retry")

RETRY_MAX_ATTEMPTS = settings.RETRY_MAX_ATTEMPTS


def with_retry(func):
    """
    Retry decorator with:
    - exponential backoff
    - jitter
    - explicit 429 handling
    - max attempts from config
    - structured logging
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 0
        max_attempts = RETRY_MAX_ATTEMPTS

        while attempts < max_attempts:
            try:
                return func(*args, **kwargs)

            except Exception as e:
                attempts += 1

                # Detect explicit 429
                is_rate_limit = (
                    hasattr(e, "response")
                    and e.response is not None
                    and getattr(e.response, "status_code", None) == 429
                )

                # Base delay: exponential backoff
                delay = 0.5 * (2 ** attempts)

                # Add jitter (0–200ms)
                jitter = random.uniform(0, 0.2)

                total_delay = delay + jitter

                logger.warning(
                    "retry_attempt",
                    function=func.__name__,
                    attempt=attempts,
                    max_attempts=max_attempts,
                    reason="rate_limit" if is_rate_limit else "exception",
                    delay_seconds=round(total_delay, 3),
                    error=str(e),
                )

                time.sleep(total_delay)

        # After max attempts → rethrow
        logger.error(
            "retry_exhausted",
            function=func.__name__,
            max_attempts=max_attempts,
        )

        raise Exception(f"Max retry attempts reached for {func.__name__}")

    return wrapper
