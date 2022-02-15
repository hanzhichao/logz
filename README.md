### Logz
Log Easy 快速上手的日志记录工具

### 特性

- 上手容易
- 日志文件按日期动态生成
- DayRottingLogger
- 记录日志到Email
- safe extra fields
- 支持多个变量
- multiline log and indent for json
- debug as default level

### 安装方法
```
$ pip install logz
```

### 使用方法
#### 简单使用

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
输出:
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

### 一次输出多个变量
```python
a = 'hello'
b = 1
c = [2]
d = {'name': 'kevin'}
log.info(a,b,c,d)
```
输出:
```
2019-12-12 22:40:20,221 INFO hello 1 [2] {'name': 'kevin'}
```

> 注意: log方法中原来支持%s格式话的变量被修改为支持log多个变量
如果你想使用原有的日志方式:
```python
import logging
logging.info('name=%s,age=%d', 'kevin',18)
```
你可以将变量直接格式化到字符串中，如下：
```python
from logz import log
log.info('name=%s,age=%d' % ('kevin',18))
```
输出:
```
2019-12-12 22:41:58,024 INFO name=kevin,age=18
```

#### 日志文件
```python
from logz import log
log.file='logs/project.log'
```
> 注意: 日志目录必须存在

By default it's a rotting file and maxBytes=10240 and backUps=5

#### 按日期记录日志
```python
from logz import log
log.file='logs/%Y-%m-%d.log'
```
And it's a day rotting file


#### 记录日志到Email中
```python
from logz import log
log.email = dict(host="smtp.sina.com", user='test_results@sina.com', password='***',
                    receivers=['superhin@126.com'], capacity=10)

for i in range(20):
    log.error('这个是个错误日志')
```

#### 修改日志等级
```
log.level = 'info'
log.level = 20
log.debug('not show')
log.info('show info')
```
输出:
```
2019-12-12 22:43:24,479 INFO show info
```

> level string is not case sensitive

#### 修改日志格式
```
log.format = '%(asctime)s %(levelname)s %(name)s %(message)s'
```

#### 使用额外字段
```
log.format = '%(asctime)s %(levelname)s %(user)s %(message)s'
log.info('hello with no user')
log.info('hello with kevin', extra={'user': 'kevin'})
```
输出:
```
2019-12-12 22:45:18,604 INFO None hello with no user
2019-12-12 22:45:18,604 INFO kevin hello with kevin
```

### 多行和字段缩进
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

#### 使用logit装饰器
```python
from logz import logit

@logit
def add(a, b):
    return a+b

def calc():
    add(1, 20)

calc()
```
输出:
```
2020-06-30 12:39:06,124 DEBUG calc -> add(1,20) return: 21 duration: 0.017280101776123047s
```

### 待完善
- log file to config maxBytes or else
- log to html
- log to db
- log diff
- log assert
- log print
- log to server using websocket
- more decorators such as @explain @exception @timeit @email
- support verbosity

