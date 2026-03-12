"""
Centralized logging configuration for FitCoach AI.

Uses Loguru for structured, colorful logging with file rotation
and different log levels for development and production.
"""

import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# Remove default logger
logger.remove()

# Log directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging(debug: bool = False):
    """
    Configure application logging.
    
    Args:
        debug: Enable debug mode with verbose logging
    """
    log_level = "DEBUG" if debug else "INFO"
    
    # Console handler with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=debug,
    )
    
    # File handler for all logs
    logger.add(
        LOG_DIR / "fitcoach_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="00:00",  # New file each day
        retention="30 days",  # Keep logs for 30 days
        compression="zip",  # Compress old logs
        backtrace=True,
        diagnose=True,
    )
    
    # Separate error log file
    logger.add(
        LOG_DIR / "errors_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="00:00",
        retention="90 days",  # Keep error logs longer
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    # API request log (for analytics)
    logger.add(
        LOG_DIR / "api_requests_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
        level="INFO",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        filter=lambda record: record["extra"].get("api_request", False),
    )
    
    logger.info(f"Logging initialized | Level: {log_level} | Debug: {debug}")


def log_api_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: int = None,
    client_ip: str = None,
):
    """
    Log API request details for analytics and monitoring.
    
    Args:
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration_ms: Request duration in milliseconds
        user_id: Authenticated user ID (if any)
        client_ip: Client IP address
    """
    log_data = {
        "method": method,
        "path": path,
        "status": status_code,
        "duration_ms": round(duration_ms, 2),
        "user_id": user_id,
        "client_ip": client_ip,
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    logger.bind(api_request=True).info(str(log_data))


def log_user_action(user_id: int, action: str, details: dict = None):
    """
    Log user actions for audit trail.
    
    Args:
        user_id: User performing the action
        action: Action description
        details: Additional action details
    """
    logger.info(f"User Action | user_id={user_id} | action={action} | details={details}")


def log_fitness_calculation(user_id: int, goal_type: str, results: dict):
    """
    Log fitness calculation for analytics.
    
    Args:
        user_id: User ID
        goal_type: Type of fitness goal
        results: Calculation results summary
    """
    logger.info(
        f"Fitness Calculation | user_id={user_id} | goal={goal_type} | "
        f"calories={results.get('calorie_target')} | bmr={results.get('bmr')}"
    )


def log_progress_entry(user_id: int, weight: float, body_fat: float = None):
    """
    Log progress entry for trend analysis.
    
    Args:
        user_id: User ID
        weight: Weight entry
        body_fat: Body fat percentage (optional)
    """
    logger.info(f"Progress Entry | user_id={user_id} | weight={weight} | body_fat={body_fat}")


# Export logger instance for use across the application
__all__ = [
    "logger",
    "setup_logging",
    "log_api_request",
    "log_user_action",
    "log_fitness_calculation",
    "log_progress_entry",
]
