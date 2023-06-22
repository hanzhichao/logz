### Logz
Log Easy 快速上手的日志记录工具

![Languate - Python](https://img.shields.io/badge/language-python-blue.svg)
![PyPI - License](https://img.shields.io/pypi/l/logz)
![PyPI](https://img.shields.io/pypi/v/logz)
![PyPI - Downloads](https://img.shields.io/pypi/dm/logz)

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
except AssertionError as ex:
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
像print函数一样,log.info等方法可以一次输出多个变量
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
log.info('name=%s,age=%d' % ('kevin',18))
```
输出:
```
2019-12-12 22:41:58,024 INFO name=kevin,age=18
```

#### 日志文件
```python
log.file='tmps/tmp.log'
log.info('info msg')
```
> 注意: 日志目录必须存在

By default it's a rotting file and maxBytes=10240 and backUps=5

#### 按日期记录日志
```python
log.file='tmps/%Y-%m-%d.log'
log.info('info msg')
```
结果是一个按天滚动的日志文件，特别对于Flask等搭建等常驻型，Web服务，日志可以按天在新的日期自动生成新的日志，而无需重启



#### 记录日志到Email中  
> 废弃 ⚠️

```python
log.email = dict(host="smtp.sina.com", user='test_results@sina.com', password='***',
                    receivers=['superhin@126.com'], capacity=10)

for i in range(20):
    log.error('这个是个错误日志')
```

#### 修改日志等级
```
log.level = 'info'
log.level = logging.INFO
log.debug('not show')
log.info('show info')
```
输出:
```
2019-12-12 22:43:24,479 INFO show info
```

> 使用字符串赋值level时大小写不敏感, `log.level = 'info'` 或 `log.level = 'INFO'`都可以

#### 修改日志格式
```
log.format = '%(levelname)s|%(filename)s|%(funcName)s|%(lineno)d|%(message)s'
```

#### 使用额外字段
```
log.format = '%(asctime)s %(levelname)s %(user)s %(message)s'
log.info('hello with no user')
log.info('hello with kevin', extra={'user': 'Kevin'})
```
输出:
```
2019-12-12 22:45:18,604 INFO None hello with no user
2019-12-12 22:45:18,604 INFO kevin hello with kevin
```

### JSON多行输出和字段缩进
```python
log.info({'foo': 'bar'}, indent=2)
```

输出:
```
2019-12-09 19:30:16,419 DEBUG log None ->
{
  "foo": "bar"
}
```

#### 使用logit装饰器
使用logit装饰器在调用函数时将自动输出`DEBUG`日志，包含调用方、调用参数，返回值，耗时信息等
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

对象方法中使用logit
```python
class Calculator(object):
    @logit
    def add(self, a, b):
        return a + b
            

Calculator.add(2,30)
```


### 待完善
- [ ] 通用extra字段及默认值配置
- log file to config maxBytes or else
- log to html
- log to db
- log diff
- log assert
- log print
- log to server using websocket
- more decorators such as @explain @exception @timeit @email
- support verbosity

### Bugs
- [ ] logit装饰器在对象方法中报错
- [ ] 还原为logging.getLogger后`%(funcName)s`字段显示不正确

### 对比
logging |logz |logzero |loguru
---| --- | --- | ---
功能 | 
易用性 | 




