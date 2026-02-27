# pylint: disable=protected-access
@type.__call__
class __getattr__:

  from importlib import import_module
  import inspect
  from types import ModuleType

  import_module = staticmethod(import_module)

  class _str(str):
    import sys
    from typing import Union

    def __getattr__(self, attr: str):
      return type(self)('.'.join((self, attr)))

    def __or__(self, other):
      return self.Union[self, other]

    def __ror__(self, other):
      return self.Union[other, self]

    def __enter__(self):
      self.sys.modules[str(self)[len(__name__) + 1:]] = self  # pyright: ignore

    def __exit__(self, *exc_info):
      self.sys.modules.pop(str(self)[len(__name__) + 1:])

    # class _str

  def _forwardref_evaluate(self) -> bool:
    frame = self.inspect.currentframe()
    while frame is not None:
      if (f_back := frame.f_back) is not None \
      and f_back.f_code.co_qualname in (
        'ForwardRef.evaluate',  # Python 3.14+
        'ForwardRef._evaluate',  # Python 3.13-
      ):
        return True
      elif frame.f_code.co_qualname == '<module>':
        return False
      frame = f_back
    return False
    # def _forwardref_evaluate -> bool

  def __call__(self, attr: str) -> str | ModuleType:
    if attr.startswith(__name__ + '.'):
      attr = attr[len(__name__) + 1:]
    if not self._forwardref_evaluate():
      return self._str('.'.join((__name__, attr)))
    return self.import_module(attr)
    # def __call__

  # class __getattr__
