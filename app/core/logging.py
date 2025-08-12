import logging
from datetime import datetime

class Request (logging.Formatter):
        def format(self, record):
                timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
                level = record.levelname
                request_id = getattr(record, 'request_id', '-')
                method = getattr(record, 'method', '-')
                path = getattr(record, 'path', '-')
                status = getattr(record, 'status', '-')
                duration_ms = getattr(record, 'duration_ms', '-')
                msg = f"{level} {timestamp} request_id={request_id} method={method} path={path} status={status} duration_ms={duration_ms}"
                return msg

logger = logging.getLogger("app_logger")
handler = logging.StreamHandler()
handler.setFormatter(Request())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_request(request_id, method, path, status, duration_ms):
        extra = {
                'request_id': request_id,
                'method': method,
                'path': path,
                'status': status,
                'duration_ms': duration_ms
        }
        logger.info('', extra=extra)

# Example usage:
# log_request('abc123', 'GET', '/health', 200, 1.7)