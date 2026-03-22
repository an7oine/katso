# pylint: disable=protected-access, invalid-name, redefined-builtin
@type.__call__
class __getattr__:

  import builtins
  import functools
  import importlib
  import inspect
  import sys
  from types import ModuleType
  from typing import Any, Callable

  _within: int = 0

  def import_string(self, name: str) -> ModuleType | Any:
    try:
      return self.importlib.import_module(name)
    except ModuleNotFoundError as exc:
      try:
        module_path, class_name = name.rsplit('.', 1)
      except ValueError:
        raise exc from None
      else:
        return getattr(
          self.import_string(module_path),
          class_name,
        )
    # def import_string

  class _str(str):
    import sys
    from types import ModuleType
    from typing import Any, Self, Union

    _modules: dict[int, ModuleType] = {}

    def __getattr__(self, attr: str) -> Any:
      global __getattr__
      return __getattr__('.'.join((self, attr)))

    def __or__(self, other):
      return self.Union[self, other]

    def __ror__(self, other):
      return self.Union[other, self]

    def __enter__(self) -> None:
      s = str(self)[len(__name__) + 1:]
      try:
        self._modules[id(self)] = self.sys.modules[s]
      except KeyError:
        pass
      self.sys.modules[s] = self  # pyright: ignore
      # def __enter__

    def __exit__(self, *exc_info: Any) -> None:
      s = str(self)[len(__name__) + 1:]
      try:
        self.sys.modules[s] = self._modules.pop(id(self))
      except KeyError:
        self.sys.modules.pop(s)
      # def __exit__

    # class _str

  def __import__(
    self,
    name: str,
    *args: Any,
    __import__: Callable[..., ModuleType],
    **kwargs: Any,
  ) -> ModuleType:
    with self._str('.'.join((__name__, name))):
      return __import__(name, *args, **kwargs)
    # def __import__

  def _defer(self) -> bool:
    if frame := self.inspect.currentframe():
      while (frame := frame.f_back) is not None:
        if not __name__ in frame.f_globals:
          continue
        if (f_back := frame.f_back) is not None \
        and f_back.f_code.co_qualname in (
          'ForwardRef._evaluate',  # Python 3.11–3.13
          'ForwardRef.evaluate',   # Python 3.14+
        ):
          return False
        if '<locals>' in frame.f_locals.get('__qualname__', ''):
          return False
        if '__module__' in frame.f_locals \
        or '__name__' in frame.f_locals:
          return True
        return False
    return False
    # def _defer -> bool

  def __call__(self, attr: str) -> str | ModuleType:
    if attr == '__path__':
      raise AttributeError(repr(attr))
    if attr.startswith(__name__ + '.'):
      attr = attr[len(__name__) + 1:]
    if self._within or self._defer():
      return self._str('.'.join((__name__, attr)))
    return self.import_string(attr)
    # def __call__

  def __enter__(self) -> None:
    self._within += 1
    self.builtins.__import__ = self.functools.wraps(
      __import__ := self.builtins.__import__
    )(
      self.functools.partial(
        self.__import__,
        __import__=__import__
      )
    )
    # def __enter__

  def __exit__(self, *exc_info: Any) -> None:
    self.builtins.__import__ = self.builtins.__import__.__wrapped__
    self._within -= 1
    # def __exit__

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
