import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict

class ApexJSONFormatter(logging.Formatter):
    """Formats log records as strict JSON for ingestion into telemetry dashboards."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        }
        return json.dumps(log_record)

def setup_logger(name: str) -> logging.Logger:
    """Initializes a standardized JSON telemetry logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ApexJSONFormatter())
        logger.addHandler(handler)
        
    return logger
