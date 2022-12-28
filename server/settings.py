import logging
import logging.config
import time


DEFAULT_ADDRESS = '0.0.0.0'
DEFAULT_PORT = 7777
MAX_CONNECTIONS = 5
MAX_PACKAGE_LENGTH = 10000
ENCODING = 'utf-8'
SALT = b'\xf1\xccd7\xf1\x1dz\x8d\\\xa6/\x85\xf8\xb9-\x14\x1e\xed~\xa7\x92\n\x05\xab{$\xb5TD\xf2\xa2<'

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


class DecorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # record.funcName == 'wrapper'
        return record.funcName == 'wrapper'


logger_config = {
    'version': 1,
    # 'disable_existing_loggers' = False,
    'formatters': {
        'std_format': {
            'format': '{asctime}::{levelname}::{name}::{module}::{funcName}::{message}',
            'style': '{'
        },
        'utc_format': {
            '()': UTCFormatter,
            # 'format': '{asctime}:{levelname}:{name}:{message}',
            'format': '{asctime}::{levelname}::{name}::{module}::{funcName}::{message}',
            'style': '{'
        },
        'utc_format_decor': {
            '()': UTCFormatter,
            'format': '{asctime}::{message}',
            'style': '{'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOGGING_CONSOLE_LVL,
            # 'formatter': 'std_format',
            'formatter': 'utc_format',
            'filters': [],
            # 'filters': ['new_filter']
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 'level': 'DEBUG',
            'level': LOGGING_FILE_LVL,
            'filename': './logs/server.log',
            'formatter': 'utc_format',
            'encoding': ENCODING,
            'utc': True,
            'when': 'MIDNIGHT'
        },
        'decor_log': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': LOGGING_FILE_LVL,
            'filename': './logs/server_decor.log',
            'formatter': 'utc_format_decor',
            'encoding': ENCODING,
            'utc': True,
            'when': 'MIDNIGHT',
            'filters': ['from_decor']
        },
        # 'file1': {
        #     '()': MyHandler,
        #     'level': 'DEBUG',
        #     'filename': 'f_debug.log',
        #     # 'formatter': 'std_format',
        #     'formatter': 'utc_format',
        # }
    },
    'loggers': {
        'server_logger': {
            'level': 'DEBUG',
            # 'level': 'NOTSET',
            # 'handlers': ['console', 'file'],
            'handlers': ['file', 'decor_log'],
            # 'propagate': False,
        }
    },

    'filters': {
        'from_decor': {
            '()': DecorFilter
        }
    }

    # 'filters': {
    #     'new_filter': {
    #         '()': NewFunctionFilter
    #     }
    # },
    # 'root': {},
    # 'incremental': True,
}
logging.config.dictConfig(logger_config)
SERVER_LOGGER = logging.getLogger('server_logger')

