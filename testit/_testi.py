import importlib
import sys
from types import ModuleType


class Testi:

  @staticmethod
  def import_string(name: str, source: str) -> ModuleType:
    spec = importlib.util.spec_from_loader(name, loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(source, module.__dict__)
    sys.modules[name] = module
    globals()[name] = module
    return module
    # def import_string

  # class Testi
