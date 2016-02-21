## Setting encoding for `sys.stdin` and `sys.stdout`

If you want `sys.stdout` to automatically use the default
encoding, you can explicitly pass an encoding name as a string (such
as `'utf-8'`) to `getwrite()` if you prefer.

```python
import locale
import codecs
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
```

For `sys.stdin`:

```python
import locale
import codecs
sys.stdin = codecs.getreader(locale.getpreferredencoding())(sys.stdin)
```
