import importlib
from inspect import get_annotations
import sys
from types import ModuleType
from typing import ForwardRef, Optional, get_type_hints

import pytest


def import_string(name: str, source: str) -> ModuleType:
  spec = importlib.util.spec_from_loader(name, loader=None)
  module = importlib.util.module_from_spec(spec)
  exec(source, module.__dict__)
  sys.modules[name] = module
  globals()[name] = module
  return module
  # def import_string


class Testi:

  @pytest.fixture
  def a(self):
    return import_string('a', '''
      from dataclasses import dataclass
      from typing import Optional
      import katso
      with katso.b:
        from b import B
      @dataclass
      class A:
        import katso
        b: Optional[B] = None
    '''.replace('\n      ', '\n'))

  @pytest.fixture
  def b(self):
    return import_string('b', '''
      from dataclasses import dataclass
      from typing import Optional
      import katso
      with katso.a:
        from a import A
      @dataclass
      class B:
        import katso
        a: Optional[A] = None
    '''.replace('\n      ', '\n'))

  def test(self, a: ModuleType, b: ModuleType):
    assert get_annotations(a.A) == {
      'b': Optional[ForwardRef('katso.b.B')],
    }
    assert get_type_hints(a.A) == {
      'b': Optional[b.B],
    }
    assert get_annotations(b.B) == {
      'a': Optional[ForwardRef('katso.a.A')],
    }
    assert get_type_hints(b.B) == {
      'a': Optional[a.A],
    }
    a = a.A(b=b.B())
    a.b.a = a
    assert repr(a) == 'A(b=B(a=...))'
    # def test

  # class Testi
