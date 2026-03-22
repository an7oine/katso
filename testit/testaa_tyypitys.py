from dataclasses import dataclass
from types import ModuleType
from typing import get_type_hints

import pytest

from ._testi import Testi


class Testi(Testi):

  @pytest.fixture
  def a(self):
    return self.import_string('a', '''
      from dataclasses import dataclass
      from typing import Self
      import katso

      with katso:
        import c as cm

      @dataclass
      class A:
        a: int
        @property
        def c(self: Self) -> cm.C:
          return cm.C(self)
    '''.replace('\n      ', '\n'))

  @pytest.fixture
  def b(self):
    return self.import_string('b', '''
      from dataclasses import dataclass
      from typing import Self
      import katso

      with katso:
        import c as cm

      @dataclass
      class B:
        b: float
        @property
        def c(self: Self) -> cm.C:
          return cm.C(self)
    '''.replace('\n      ', '\n'))

  @pytest.fixture
  def c(self):
    return self.import_string('c', '''
      from dataclasses import dataclass
      import katso

      with katso:
        import a as am
        import b as bm

      @dataclass
      class C:
        c: am.A | bm.B
        d: None | am.A | bm.B = None
    '''.replace('\n      ', '\n'))

  def test(self, a: ModuleType, b: ModuleType, c: ModuleType):
    ai = a.A(42)
    bi = b.B(5.7)
    assert get_type_hints(c.C) == {'c': a.A | b.B, 'd': None | a.A | b.B}
    assert isinstance(ai.c, c.C) and isinstance(ai.c.c, a.A)
    assert isinstance(bi.c, c.C) and isinstance(bi.c.c, b.B)
    # def test

  # class Testi
