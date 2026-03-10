from inspect import get_annotations
import sys
from types import ModuleType
from typing import ForwardRef, Optional, get_type_hints

import pytest

from ._testi import Testi


class Testi(Testi):

  @pytest.fixture
  def a(self):
    return self.import_string('a', '''
      from dataclasses import dataclass
      import sys
      from typing import Optional, Self
      import katso
      with katso:
        import b as bm
      @dataclass
      class A:
        b: Optional[bm.B] = None
        def __add__(self: Self, toinen: Optional[Self]) -> Self:
          if self.b is None or toinen is None:
            return toinen or self
          return A(b=bm.B(a=toinen))
    '''.replace('\n      ', '\n'))

  @pytest.fixture
  def b(self):
    return self.import_string('b', '''
      from dataclasses import dataclass
      import sys
      from typing import Optional, Self
      import katso
      with katso:
        import a as am
      @dataclass
      class B:
        a: Optional[am.A] = None
        def __add__(self: Self, toinen: Optional[Self]) -> Self:
          if self.a is None or toinen is None:
            return toinen or self
          return B(a=am.A(b=self))
    '''.replace('\n      ', '\n'))

  def test(self, a: ModuleType, b: ModuleType):
    if sys.version_info >= (3, 14):
      assert get_annotations(a.A) == {
        'b': Optional[b.B]
      }
    else:
      assert get_annotations(a.A) == {
        'b': Optional[ForwardRef('katso.b.B')],
      }
    assert get_type_hints(a.A) == {
      'b': Optional[b.B],
    }
    if sys.version_info >= (3, 14):
      assert get_annotations(b.B) == {
        'a': Optional[a.A]
      }
    else:
      assert get_annotations(b.B) == {
        'a': Optional[ForwardRef('katso.a.A')],
      }
    assert get_type_hints(b.B) == {
      'a': Optional[a.A],
    }
    a1 = a.A(b=b.B())
    a1.b.a = a1
    b2 = b.B(a=a.A())
    b2.a.b = b2
    assert repr(a1) == 'A(b=B(a=...))'
    assert repr(b2) == 'B(a=A(b=...))'
    ab1 = a1 + b2.a
    ba2 = a1.b + b2
    assert repr(ab1) == 'A(b=B(a=A(b=B(a=...))))'
    assert repr(ba2) == 'B(a=A(b=B(a=A(b=...))))'
    # def test

  # class Testi
