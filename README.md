katso
=====

```python
# lib/am.py

from dataclasses import dataclass
from typing import Optional

import katso

with katso:
  from lib import bm


@dataclass(kw_only=True)
class A:
  a: int
  b: Optional[bm.B] = None


# lib/bm.py

from dataclasses import dataclass
from typing import Optional

import katso

with katso:
  from lib import am


@dataclass(kw_only=True)
class B:
  a: Optional[am.A] = None
  b: str


# bin/cm.py

from dataclasses import dataclass

from lib import am, bm


@dataclass
class C:
  a: am.A
  b: bm.B

  def __post_init__(self):
    self.a.b = self.b
    self.b.a = self.a
    # def __init__

  # class C


c = C(am.A(a=42), bm.B(b='spam'))
assert str(c) == "C(a=A(a=42, b=B(a=..., b='spam')), b=B(a=A(a=42, b=...), b='spam'))"
```
