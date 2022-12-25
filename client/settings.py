import logging.config
import time


DEFAULT_PORT = 7777
MAX_PACKAGE_LENGTH = 10000
ENCODING = 'utf-8'
TIMEOUT = 10


# Уровень логирования:
# 'CRITICAL' 50
# 'ERROR' 40
# 'WARNING' 30
# 'INFO' 20
# 'DEBUG' 10
# 'NOTSET' 0
LOGGING_CONSOLE_LVL = 'CRITICAL'
LOGGING_FILE_LVL = 'DEBUG'

class UTCFormatter(logging.Formatter):
    """
    Форматер с конвертацией времени в UTC(GMT)
    """
    converter = time.gmtime


logger_config = {
    'version': 1,
    # 'disable_existing_loggers' = False,
    'formatters': {
        'utc_format': {
            '()': UTCFormatter,
            # 'format': '{asctime}:{levelname}:{name}:{message}',
            'format': '{asctime}::{levelname}::{name}::{module}::{funcName}::{message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOGGING_CONSOLE_LVL,
            'formatter': 'utc_format',
            'filters': [],
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': LOGGING_FILE_LVL,
            'filename': './logs/client.log',
            'formatter': 'utc_format',
            'encoding': ENCODING,
            'utc': True,
            'when': 'MIDNIGHT'
        }
    },
    'loggers': {
        # client_logger
        'client_logger': {
            'level': 'DEBUG',
            'handlers': ['file'],
        }
    }
}
logging.config.dictConfig(logger_config)
CLIENT_LOGGER = logging.getLogger('client_logger')
