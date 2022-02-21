import os
from pprint import pprint

from logz import log, logit, LOGGER_NAME
import logging
import pytest
import re
from email.mime.text import MIMEText

# log.format = '%(asctime)s %(name)s %(levelname)s %(filename)s [%(funcName)s] %(lineno)d %(message)s'


def test_log_message(caplog):
    """测试简单使用"""
    log.debug('debug msg')
    log.info('info msg')
    log.warning('warning msg')
    log.error('error msg')
    log.critical('critical msg')
    try:
        assert 0
    except AssertionError as ex:
        log.exception(ex)
        
    print(caplog.record_tuples)
    assert caplog.record_tuples == [(LOGGER_NAME, logging.DEBUG, 'debug msg'),
                                    (LOGGER_NAME, logging.INFO, 'info msg'),
                                    (LOGGER_NAME, logging.WARNING, 'warning msg'),
                                    (LOGGER_NAME, logging.ERROR, 'error msg'),
                                    (LOGGER_NAME, logging.CRITICAL, 'critical msg'),
                                    (LOGGER_NAME, logging.ERROR, 'assert 0')]
    
    
def test_log_multiple_variables(caplog):
    """测试一次输出多个变量"""
    a = 'hello'
    b = 1
    c = [2]
    d = {'name': 'kevin'}
    log.info(a, b, c, d)
    print(caplog.record_tuples)
    assert caplog.record_tuples == [(LOGGER_NAME, logging.INFO, "hello 1 [2] {'name': 'kevin'}")]


def test_log_file(tmp_path):
    """测试日志文件"""
    log.file = tmp_path / 'tmp.log'
    log.info('info msg')
    with open(log.file, encoding='utf-8') as f:
        records = f.read()
    print('records', records)
    assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} INFO info msg\n', records) is not None


def test_day_rotting_log_file(tmp_path):
    """测试按日期记录日志"""
    log.file = tmp_path / '%Y-%m-%d.log'
    log.info('info msg')
    assert re.match(r'\d{4}-\d{2}-\d{2}.log', os.path.basename(log.file)) is not None
    with open(log.file, encoding='utf-8') as f:
        records = f.read()
    print('records', records)
    assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} INFO info msg\n', records) is not None


@pytest.mark.xfail(reason='SMTP密钥失效')
def test_log_email():
    log.email = dict(host="smtp.sina.com", user='test_results@sina.com', password='5cfd63dc622c1a2f',
                    receivers='hanzhichao@secoo.com', count=10)

    for i in range(20):
        log.error('这个是个错误日志')


def test_set_log_level(caplog):
    """测试修改日志等级"""
    log.level = 'info'
    log.debug('not show')
    log.info('show info')
    print(caplog.record_tuples)
    assert caplog.record_tuples == [('logz', 20, 'show info')]

    caplog.clear()
    log.level = logging.INFO
    log.debug('not show')
    log.info('show info')
    print(caplog.record_tuples)
    assert caplog.record_tuples == [('logz', 20, 'show info')]
    
    
def test_set_log_format(caplog):
    log.format = '%(levelname)s|%(filename)s|%(funcName)s|%(lineno)d|%(message)s'
    log.info('info msg')
    print(caplog.text.strip())
    assert re.match(r'INFO|__init__.py|log|\d+|info msg', caplog.text.strip())


def test_log_with_extra(caplog):
    """测试使用额外字段"""
    log.format = '%(asctime)s %(levelname)s %(user)s %(message)s'
    log.info('hello with no user')
    log.info('hello with kevin', extra={'user': 'Kevin'})
    log.extra = {'user': 'hzc'}
    log.info('hello with no user')
    log.info('hello with kevin', extra={'user': 'Kevin'})
    assert getattr(caplog.records[0], 'user') is None
    assert getattr(caplog.records[1], 'user') == 'Kevin'
    assert getattr(caplog.records[2], 'user') == 'hzc'
    assert getattr(caplog.records[3], 'user') == 'Kevin'
    
    
def test_log_multi_lines(caplog):
    """测试JSON多行输出和字段缩进"""
    log.info({'foo': 'bar'}, indent=2)
    excepted_msg = '\n'.join(['->', '{', '  "foo": "bar"', '}'])
    assert caplog.record_tuples == [(LOGGER_NAME, logging.INFO, excepted_msg)]


def test_function_with_logit(caplog):
    """测试函数使用logit装饰器"""
    @logit
    def add(a, b):
        return a + b

    def calc():
        add(1, 20)

    calc()
    print(caplog.records[0].msg)
    assert re.match(r'calc -> add\(1,20\) return: 21 duration: \d+.\d+s',
                    caplog.records[0].msg) is not None


@pytest.mark.xfail(reason='待修复')
def test_method_with_logit(caplog):  # Fixme
    """测试对象方法使用logit装饰器"""
    class Calculator(object):
        @logit
        def add(self, a, b):
            return a + b

    Calculator.add(2, 30)





