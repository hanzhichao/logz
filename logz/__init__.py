"""日志配置"""
import re
import json
from datetime import datetime
import time
import inspect
import logging
from functools import wraps
from logging.handlers import BaseRotatingHandler

LOG_ITEMS = ('name', 'levelno', 'levelname', 'pathname', 'filename', 'funcName',
             'lineno', 'asctime', 'thread', 'threadName', 'process', 'message')


LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


class DayRotatingHandler(BaseRotatingHandler):
    def __init__(self, filename, mode, encoding=None, delay=False):
        self.filename = filename
        self.date = datetime.now().date()
        super().__init__(filename, mode, encoding, delay)

    def shouldRollover(self, record):
        return self.date != datetime.now().date()

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.baseFilename = self.date.strftime(self.filename)
        self._open()


class HTMLHandler(logging.FileHandler):
    pass


class Log(object):
    def __init__(self, name=__name__):
        self.name = name
        self.__logger = logging.getLogger(name)
        self.__format = logging.Formatter(LOG_FORMAT)
        self.__level = logging.DEBUG
        self.__extra = None
        self.__file = None

        self.verbosity = None
        self.filter = None
        self.hook = None  # todo
        self.html = None
        self.email = None
        self.db = None
        self.server = None

        ch = logging.StreamHandler()
        ch.setFormatter(self.__format)

        self.__logger.setLevel(self.__level)
        self.__logger.addHandler(ch)

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        if isinstance(value, int) and value in (0,10,20,30,40,50):
            self.__level = value
        if isinstance(value, str):
            value = value.lower()
            if value == 'debug':
                self.__level = logging.DEBUG
            elif value == 'info':
                self.__level = logging.INFO
            elif value in ('warn', 'warning'):
                self.__level = logging.WARNING
            elif value == 'error':
                self.__level = logging.ERROR
            elif value == 'critical':
                self.__level = logging.CRITICAL
        self.__logger.setLevel(self.__level)

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, value):
        items = re.findall(r'%\((.*?)\)s', value)
        self.__extra = {key: None for key in (set(items)-set(LOG_ITEMS))}
        self.__format = logging.Formatter(value)

        for handler in self.__logger.handlers:
            handler.setFormatter(self.__format)

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):  # todo
        if '%' in value:
            value = datetime.now().strftime(value)
            fh = DayRotatingHandler(value, 'a', encoding='utf-8')
        else:
            fh = logging.handlers.RotatingFileHandler(value, 'a', encoding='utf-8', maxBytes=10240, backupCount=5)
        fh.setFormatter(self.__format)
        self.__file = value
        self.__logger.addHandler(fh)

    @property
    def logger(self):
        return self.__logger

    def log(self, level, msg, *args, **kwargs):
        if args:
            msg = '%s %s' % (str(msg), ' '.join([str(arg) for arg in args]))
        if self.__extra:
            extra = kwargs.get('extra', {})
            kwargs['extra'] = self.__extra
            kwargs['extra'].update(extra)

        if 'indent' in kwargs:  # todo
            indent = kwargs.pop('indent')
            if indent and isinstance(msg, dict):
                msg = '->\n' + json.dumps(msg, indent=indent, ensure_ascii=False)

        if level == 'critical':
            self.__logger.critical(msg, **kwargs)
        elif level == 'error':
            self.__logger.error(msg, **kwargs)
        elif level == 'exception':
            self.__logger.exception(msg, **kwargs)
        elif level == 'warning':
            self.__logger.warning(msg, **kwargs)
        elif level == 'info':
            self.__logger.info(msg, **kwargs)
        else:
            self.__logger.debug(msg, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.log('debug', msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log('info', msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.log('warning', msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log('warning', msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log('error', msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.log('exception', msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log('critical', msg, *args, **kwargs)


log = Log()


def _to_string(args, kwargs):
    params = []
    for arg in args:
        params.append(str(arg))
    for k, v in kwargs.items():
        params.append(f'{k}={v}')
    return ','.join(params)


def logit():
    def _log_action(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            parent_action = inspect.stack()[1][3].strip()

            result = func(*args, **kwargs)
            logging.info(f"{parent_action} -> {func.__name__}({_to_string(args, kwargs)}) return: {result} "
                     f"duration: {time.time() - start}s")

            return result
        return wrapper
    return _log_action


if __name__ == '__main__':
    log.format = '%(asctime)s %(levelname)s %(user)s %(message)s'
    log.info('hello with no user')
    log.info('hello with kevin', extra={'user': 'kevin'})
