# logz
easy use for log with extra infos

## Features

- very easy to use
- log file name change from date
- DayRottingLogger
- log to email
- safe extra fields
- log multi vars and not just str
- multiline log and indent for json
- debug as default level

## Install
```
$ pip install logz
```

## Use
### Simple Use

```python
from logz import log
log.debug('debug msg')
log.info('info msg')
log.warning('warning msg')
log.error('error msg')
log.critical('critical mst')
try:
    assert 0
except AttributeError as ex:
    log.exception(ex)
```
output:
```
2019-12-12 22:39:43,584 DEBUG debug msg
2019-12-12 22:39:43,584 INFO info msg
2019-12-12 22:39:43,584 WARNING warning msg
2019-12-12 22:39:43,585 ERROR error msg
2019-12-12 22:39:43,585 CRITICAL critical mst
Traceback (most recent call last):
  File "/Users/apple/Documents/Projects/logz/logz/__init__.py", line 199, in <module>
    assert 0
AssertionError
```

### log multi vars one time
```python
a = 'hello'
b = 1
c = [2]
d = {'name': 'kevin'}
log.info(a,b,c,d)
```
output:
```
2019-12-12 22:40:20,221 INFO hello 1 [2] {'name': 'kevin'}
```

> Note: Change args form supporting %s format to supporting multi vars
if you want to use something like:
```python
import logging
logging.info('name=%s,age=%d', 'kevin',18)
```
you neet use like below:
```python
from logz import log
log.info('name=%s,age=%d' % ('kevin',18))
```
output:
```
2019-12-12 22:41:58,024 INFO name=kevin,age=18
```

### log to file
```python
from logz import log
log.file='logs/project.log'
```
> Note: logs directory must be exists

By default it's a rotting file and maxBytes=10240 and backUps=5

### log to a file with name changes with date
```python
from logz import log
log.file='logs/%Y-%m-%d.log'
```
And it's a day rotting file


### log to email 
```python
from logz import log
log.email = dict(host="smtp.sina.com", user='test_results@sina.com', password='***',
                    receivers=['superhin@126.com'], capacity=10)

for i in range(20):
    log.error('这个是个错误日志')
```

### change log level
```
log.level = 'info'
log.level = 20
log.debug('not show')
log.info('show info')
```
output:
```
2019-12-12 22:43:24,479 INFO show info
```

> level string is not case sensitive

### change log format
```
log.format = '%(asctime)s %(levelname)s %(name)s %(message)s'
```

### with extra fields
```
log.format = '%(asctime)s %(levelname)s %(user)s %(message)s'
log.info('hello with no user')
log.info('hello with kevin', extra={'user': 'kevin'})
```
output:
```
2019-12-12 22:45:18,604 INFO None hello with no user
2019-12-12 22:45:18,604 INFO kevin hello with kevin
```

### multiline and indent for dict
```python
from logz import log
log.info({'foo': 'bar'}, indent=2)
```

output:
```
2019-12-09 19:30:16,419 DEBUG log None ->
{
  "foo": "bar"
}
```

### user logit
```python
from logz import logit

@logit
def add(a, b):
    return a+b

def calc():
    add(1, 20)

calc()
```
output:
```
2020-06-30 12:39:06,124 DEBUG calc -> add(1,20) return: 21 duration: 0.017280101776123047s
```

## todo
- log file to config maxBytes or else
- log to html
- log to db
- log diff
- log assert
- log print
- log to server using websocket
- more decorators such as @explain @exception @timeit @email
- support verbosity

