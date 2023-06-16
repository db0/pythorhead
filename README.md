# Pythörhead

A python library for interacting with Lemmy

![pythorhead logo](https://raw.githubusercontent.com/db0/pythorhead/main/logo.png)

# Sample Usage

```python
from pythorhead import Lemmy

lemmy = Lemmy("https://lemmy.dbzer0.com")
lemmy.log_in("username", "password")
community_id = lemmy.discover_community("botart")
lemmy.post.create(community_id, "Hello Lemmy World")
```
