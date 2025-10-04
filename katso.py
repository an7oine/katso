# pylint: disable=protected-access
@type.__call__
class __getattr__:

  from importlib import import_module
  from types import ModuleType

  import_module = staticmethod(import_module)

  class _str(str):
    def __getattr__(self, attr: str):
      return type(self)('.'.join((self, attr)))

  class _module(ModuleType):
    def __getattr__(self, attr: str):
      try:
        return super().__getattr__(attr)
      except AttributeError:
        global __getattr__
        return __getattr__('.'.join((self.__name__, attr)))

  def __call__(self, attr: str):
    if attr.startswith(__name__ + '.'):
      attr = attr[len(__name__) + 1:]
    try:
      module = self.import_module(attr)
    except ModuleNotFoundError:
      return self._str('.'.join((__name__, attr)))
    else:
      _module = self._module(module.__name__)
      _module.__dict__.update(module.__dict__)
      return _module
    # def __call__

  # class __getattr__
