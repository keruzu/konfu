import logging
from pythonjsonlogger import jsonlogger


def defaultLogger(level='debug'):
    'No config log handler'
    log = logging.getLogger('')

    logHandler = logging.StreamHandler()
    format = '%(asctime)s %(filename)s %(levelname)s %(message)s'
    formatter = jsonlogger.JsonFormatter(format)
    logHandler.setFormatter(formatter)
    log.addHandler(logHandler)

    level = level.upper()
    level = getattr(logging, level, None)
    if level:
        log.setLevel(level)
    else:
        log.setLevel(logging.DEBUG)
    return log

