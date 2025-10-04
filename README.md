katso
=====

```python
# lib/a.py
from dataclasses import dataclass
from typing import Optional

import katso

@dataclass(kw_only=True)
class A:
  a: int
  b: Optional[katso.lib.b.B] = None


# lib/b.py
from dataclasses import dataclass
from typing import Optional

import katso

@dataclass(kw_only=True)
class B:
  a: Optional[katso.lib.a.A] = None
  b: str


# bin/c.py
from dataclasses import dataclass

import katso

def f(a: katso.lib.a.A, b: katso.lib.b.B) -> katso.bin.c.C:
  return C(a, b)

@dataclass
class C:
  a: katso.lib.a.A
  b: katso.lib.b.B

  def __post_init__(self):
    self.a.b = self.b
    self.b.a = self.a
    # def __init__

  # class C


from lib.a import A
from lib.B import B
c = f(A(a=42), B(b=57))
print(c)  # C(a=A(a=42, b=B(a=..., b=57)), b=B(a=A(a=42, b=...), b=57))
```
