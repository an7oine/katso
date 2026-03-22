from types import ModuleType

import pytest

from ._testi import Testi


class Testi(Testi):

  @pytest.fixture
  def a(self):
    return self.import_string('a', '''
      from dataclasses import dataclass
      import katso

      with katso:
        import a as am
        import b as bm

      @dataclass
      class A:
        a: int
        def b(self: am.A, b: bm.B) -> bm.B:
          return bm.B(b=self.a + b.b)
    '''.replace('\n      ', '\n'))

  @pytest.fixture
  def b(self):
    return self.import_string('b', '''
      from dataclasses import dataclass
      import katso

      with katso:
        import a as am
        import b as bm

      @dataclass
      class B:
        b: int
        def a(self: bm.B, a: am.A) -> am.A:
          return am.A(a=self.b - a.a)
    '''.replace('\n      ', '\n'))

  def test(self, a: ModuleType, b: ModuleType):
    ai = a.A(42)
    bi = b.B(57)

    bj = ai.b(bi)
    aj = bi.a(ai)

    assert isinstance(aj, a.A)
    assert isinstance(bj, b.B)
    assert repr(aj) == 'A(a=15)'
    assert repr(bj) == 'B(b=99)'
    # def test

  # class Testi
