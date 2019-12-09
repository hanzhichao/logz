# log

> pip install logz


```python
from logz import log

log.file = 'logs/%Y-%m-%d.log'
log.level = 'info'
log.format = '%(levelname)s %(name)s %(user)s %(message)s'
log.file = '%Y-%m-%d.html'
log.debug({'foo': 'bar'}, indent=2)
log.info("hello", extra={'user': 'hanzhichao'})

```

output:
```
2019-12-09 19:30:16,419 DEBUG log None ->
{
  "foo": "bar"
}
2019-12-09 19:30:16,419 INFO log hanzhichao hello
```
