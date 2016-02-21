If you want `sys.stdout` to automatically use the default
encoding. You can explicitly pass an encoding name as a string (such
as `'utf-8'`) to `getwrite()` if you prefer.

```python
import locale
import codecs
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
```

Same thing for `sys.stdin`.
