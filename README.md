# pythorhead

A python library for interacting with Lemmy

# Sample Usage

```python
from pythorhead import Lemmy

lemmy = Lemmy("https://lemmy.example.com")
lemmy.log_in("username", "password")
community_id = lemmy.discover_community("botart")
lemmy.post(community_id, "Hello Lemmy World")
```