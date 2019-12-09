from logext666.log import log, log_action


log.file = '%Y-%m-%d.log'
log.level = 'debug'
log.format = '%(asctime)s %(levelname)s %(name)s %(user)s %(message)s'
log.file = '%Y-%m-%d.html'
log.debug({'foo': 'bar'}, indent=2)
log.info("hello", extra={'user': 'hanzhichao'})


@log_action()
def bar(arg):
    return arg


@log_action()
def foo(arg):
    return bar(arg)


if __name__ == '__main__':
    foo('hello,log')
