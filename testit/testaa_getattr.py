from dataclasses import dataclass
import importlib
from inspect import get_annotations
import sys
from types import ModuleType
from typing import ForwardRef, Optional, get_type_hints

import pytest

import katso


def import_string(name: str, source: str):
  spec = importlib.util.spec_from_loader(name, loader=None)
  module = importlib.util.module_from_spec(spec)
  exec(source, module.__dict__)
  sys.modules[name] = module
  globals()[name] = module
  return module
  # def import_string


class TestAB:

  @dataclass
  class A:
    b: Optional[katso.testit.testaa_getattr.TestAB.B] = None

  @dataclass
  class B:
    a: Optional[katso.testit.testaa_getattr.TestAB.A] = None

  def test(self):
    assert get_annotations(self.A) == {
      'b': Optional[ForwardRef('katso.testit.testaa_getattr.TestAB.B')]
    }
    assert get_type_hints(self.A) == {
      'b': Optional[self.B]
    }
    assert get_annotations(self.B) == {
      'a': Optional[ForwardRef('katso.testit.testaa_getattr.TestAB.A')]
    }
    assert get_type_hints(self.B) == {
      'a': Optional[self.A]
    }
    a = self.A(b=self.B())
    a.b.a = a
    assert repr(a) == 'TestAB.A(b=TestAB.B(a=...))'
    # def new

  # class TestAB


class TestCD:

  @pytest.fixture
  def c(self):
    return import_string('c', '''
      from dataclasses import dataclass
      from typing import Optional
      import katso
      @dataclass
      class C:
        d: Optional[katso.d.D] = None
    '''.replace('\n      ', '\n'))

  @pytest.fixture
  def d(self):
    return import_string('d', '''
      from dataclasses import dataclass
      from typing import Optional
      import katso
      @dataclass
      class D:
        c: Optional[katso.c.C] = None
    '''.replace('\n      ', '\n'))

  def test(self, c: ModuleType, d: ModuleType):
    assert get_type_hints(c.C) == {
      'd': Optional[d.D]
    }
    assert get_type_hints(d.D) == {
      'c': Optional[c.C]
    }
    c = c.C(d=d.D())
    c.d.c = c
    assert repr(c) == 'C(d=D(c=...))'
    # def test

  # class TestCD
