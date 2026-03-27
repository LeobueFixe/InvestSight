import logging
import time
import uuid
from contextlib import contextmanager
from typing import Optional

import structlog

from apps.apis.config import LOG_LEVEL


structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


def get_logger(name: str) -> logging.Logger:
    return structlog.get_logger(name)


@contextmanager
def log_api_call(symbol: str, provider: str):
    correlation_id = str(uuid.uuid4())
    logger = get_logger("api_call")
    start_time = time.time()

    logger.info(
        "API call started",
        symbol=symbol,
        provider=provider,
        correlation_id=correlation_id,
    )

    try:
        yield
        latency_ms = (time.time() - start_time) * 1000
        logger.info(
            "API call completed",
            symbol=symbol,
            provider=provider,
            correlation_id=correlation_id,
            latency_ms=round(latency_ms, 2),
            status="success",
        )
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        logger.error(
            "API call failed",
            symbol=symbol,
            provider=provider,
            correlation_id=correlation_id,
            latency_ms=round(latency_ms, 2),
            status="error",
            error=str(e),
        )
        raise
