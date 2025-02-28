import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(log_name, log_file: str = None, level=logging.INFO):
    """
    Sets up a logger with both console and file handlers.
    
    Args:
        log_name: Name of the logger
        log_file: Path to log file (optional)
        level: Logging level (default: INFO)
    
    Returns:
        Logger instance
    """
    # Create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger