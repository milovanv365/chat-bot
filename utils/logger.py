import os
import sys
import datetime
import logging
from .constants import LOG_DIR
from logging.handlers import RotatingFileHandler

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

_log_fn = os.path.join(LOG_DIR, 'chat-bot.log')
handler = RotatingFileHandler(filename=_log_fn, mode='a', maxBytes=5*1024*1024,
                              backupCount=2, encoding=None, delay=0)
_log_formatter = logging.Formatter(fmt='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(fmt=_log_formatter)
handler.setLevel(level=logging.INFO)

logger = logging.getLogger('NLP')
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def __log_msg(prefix, msg):
    if len(msg) > 0 and msg[0] == '\r':
        msg = msg[1:]
    _t_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sys.stdout.write("{} :: {} :: {}\n".format(_t_str, prefix, msg))
    return msg


def info(msg):
    logger.info(__log_msg("INFO", msg))


def warn(msg):
    logger.warning(__log_msg("WARN", msg))


def error(msg):
    logger.error(__log_msg("ERROR", msg))
