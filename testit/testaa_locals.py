from types import ModuleType

import pytest

from ._testi import Testi


class Testi(Testi):

  @pytest.fixture
  def mod(self):
    return self.import_string('mod', '''
      from dataclasses import dataclass
      import katso

      with katso:
        import mod

      @dataclass
      class A:
        a: int

      def b(a: int) -> type:
        @dataclass
        class B:
          a: mod.A
        return B(mod.A(a))
    '''.replace('\n      ', '\n'))

  def test(self, mod: ModuleType):
    assert isinstance(mod.b(42).a, mod.A)

  # class Testi
