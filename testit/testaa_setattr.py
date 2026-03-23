from dataclasses import dataclass
from inspect import get_annotations
import katso


class Testi:

  def test(self):
    try:
      katso.attr = 'val'
    except AttributeError:
      pass
    else:
      assert False
    # def new

  # class Testi
