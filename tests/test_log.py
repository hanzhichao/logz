from logz import log, logit
import logging
from email.mime.text import MIMEText

log.format = '%(asctime)s %(name)s %(levelname)s %(filename)s [%(funcName)s] %(lineno)d %(message)s'


def test_log_function():
    log.info('hello, moto')


@logit
def add(a, b):
    log.info('a+b=', a+b)
    return a+b

class Demo(object):
    @logit
    def add(self, a, b):
        log.info('a+b=', a + b)
        return a + b

def test_logit():
    log.info('hello, logit')
    sum = add(1, 20)
    logging.info(sum)


def calc():
    sum = add(1, 20)
    d = Demo()
    d.add(2, 30)


def test_log_smtp():
    log.email = dict(host="smtp.sina.com", user='test_results@sina.com', password='5cfd63dc622c1a2f',
                    receivers='hanzhichao@secoo.com', count=10)

    for i in range(20):
        log.error('这个是个错误日志')

test_log_smtp()