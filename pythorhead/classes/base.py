from dataclasses import dataclass, asdict, field
from pythorhead.utils import json_serializer

import json


@dataclass
class LemmyBaseClass:
    # The owning lemmy instance. We use it to reach the API classes
    _lemmy: 'Lemmy' = field(init=None)
    # The original data dict from which we created this class
    _origin: dict = field(init=None)
    
    def asdict(self):
        selfdict = asdict(self)
        del selfdict['_lemmy']
        del selfdict['_origin']
        return selfdict

    def asjson(self, indent=4):      
        return json.dumps(self.asdict(), indent=indent, default=json_serializer)
    