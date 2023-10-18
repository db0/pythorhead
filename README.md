# Pythörhead

A python library for interacting with Lemmy

![pythorhead logo](https://raw.githubusercontent.com/db0/pythorhead/main/logo.png)

# Examples

See working examples in [examples/](https://github.com/db0/pythorhead/tree/main/examples)


# Exceptions

If you want to raise exceptions on failures instead of returning null, pass `raise_exceptions=True` to the `Lemmy()` constructor.

The normal request timeout is 3 seconds. If you want to change this number, you can set it on the constructor uising `request_timeout=`

## Sample Post Usage

```python
from pythorhead import Lemmy

lemmy = Lemmy("https://lemmy.dbzer0.com",request_timeout=2)
lemmy.log_in("username", "password")
community_id = lemmy.discover_community("botart")
lemmy.post.create(community_id, "Hello Lemmy World")
```

## Sample Comment Usage

```python
from pythorhead import Lemmy

lemmy = Lemmy("https://lemmy.dbzer0.com")
lemmy.log_in("username", "password")

# getting the first post id
post_id = lemmy.post.list()[0]["post"]["id"]

# leave a comment
lemmy.comment.create(post_id, "Hello Lemmy World")

```

