# pylint: disable=protected-access, invalid-name, redefined-builtin
@type.__call__
class __getattr__:

  import builtins
  import functools
  from importlib import import_module
  import inspect
  import sys
  from types import ModuleType

  import_module = staticmethod(import_module)

  class _str(str):
    import sys
    from types import ModuleType
    from typing import Union

    _modules: dict[int, ModuleType] = {}

    def __getattr__(self, attr: str):
      return type(self)('.'.join((self, attr)))

    def __or__(self, other):
      return self.Union[self, other]

    def __ror__(self, other):
      return self.Union[other, self]

    def __enter__(self):
      s = str(self)[len(__name__) + 1:]
      try:
        self._modules[id(self)] = self.sys.modules[s]
      except KeyError:
        pass
      self.sys.modules[s] = self  # pyright: ignore
      # def __enter__

    def __exit__(self, *exc_info):
      s = str(self)[len(__name__) + 1:]
      try:
        self.sys.modules[s] = self._modules.pop(id(self))
      except KeyError:
        self.sys.modules.pop(s)
      # def __exit__

    # class _str

  def __import__(self, name, *args, __import__, **kwargs):
    with self._str('.'.join((__name__, name))):
      return __import__(name, *args, **kwargs)
    # def __import__

  def _annotate(self) -> bool:
    # Python 3.14+
    if frame := self.inspect.currentframe():
      while (frame := frame.f_back) is not None:
        if frame.f_code.co_name == '__annotate__':
          return True
    return False
    # def _annotate -> bool

  def _forwardref_evaluate(self) -> bool:
    # Python 3.13-
    frame = self.inspect.currentframe()
    while frame is not None:
      if (f_back := frame.f_back) is not None \
      and f_back.f_code.co_qualname == 'ForwardRef._evaluate':
        return True
      elif frame.f_code.co_qualname == '<module>':
        return False
      frame = f_back
    return False
    # def _forwardref_evaluate -> bool

  def _defer(self) -> bool:
    if self.sys.version_info >= (3, 14):
      return self._annotate()
    else:
      return not self._forwardref_evaluate()
    # def _defer -> bool

  def __call__(self, attr: str) -> str | ModuleType:
    if attr.startswith(__name__ + '.'):
      attr = attr[len(__name__) + 1:]
    if self._defer():
      return self._str('.'.join((__name__, attr)))
    return self.import_module(attr)
    # def __call__

  def __enter__(self):
    self.builtins.__import__ = self.functools.wraps(
      __import__ := self.builtins.__import__
    )(
      self.functools.partial(
        self.__import__,
        __import__=__import__
      )
    )
    # def __enter__

  def __exit__(self, *exc_info):
    self.builtins.__import__ = self.builtins.__import__.__wrapped__

  # class __getattr__


__getattr__.sys.modules[__name__].__class__ = __getattr__.functools.wraps(
  __getattr__.sys.modules[__name__].__class__,
  updated=()
)(type(
  __getattr__.sys.modules[__name__].__class__.__name__,
  (
    __getattr__.sys.modules[__name__].__class__,
  ),
  {
    '__enter__': __getattr__.__enter__,
    '__exit__': __getattr__.__exit__,
  }
))
