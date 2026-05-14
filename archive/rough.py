from __future__ import annotations
import inspect
import keyword
from enum import Enum
import types
import builtins



MISSING = object()

def _is_valid_python_name(name):
    if not isinstance(name, str):
        raise ValueError(f"name must be of type str, not {type(name).__name__}")
    if not name.isidentifier():
        raise ValueError(f"{name} is not a valid identifier")
    if keyword.iskeyword(name):
        raise ValueError(f"{name} is a Python keyword")
    return True

def field_to_string(val):
    if isinstance(val, str):
        return val
    if val is None:
        return "None"
    if val is Ellipsis:
        return "..."
    if isinstance(val, type):
        if val.__module__ == "builtins":
            return val.__qualname__
        return f"{val.__module__}.{val.__qualname__}"
    return repr(val)


class Param:

    def __init__(self, name : str, kind : ParamKind, * , annotation: object = MISSING, default_val: object = MISSING):
        _is_valid_python_name(name)
        self._name = name
        self._kind = kind
        self._annotation = annotation
        self._default = default_val

    def has_default(self):
        return self._default is not MISSING
    
    def has_annotation(self):
        return self._annotation is not MISSING
    

    def __str__(self):
        s = self._name
        if self.has_annotation():
            x = field_to_string(self._annotation)
            s += f": {x}"
        if self.has_default():
            s += f" = {str(self._default)}"
        return s

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, val):
        _is_valid_python_name(val)
        self._name = val

    @property
    def kind(self):
        return self._kind
    @kind.setter
    def kind(self, val):
        if not isinstance(val, ParamKind):
            raise ValueError(f"val must be of type {ParamKind.__name__}")
        self._kind = val
        
    @property
    def annotation(self):
        return self._annotation
    @annotation.setter
    def annotation(self, val):
        self._annotation = val
    @annotation.deleter
    def annotation(self):
        self._annotation = MISSING

    @property
    def default(self):
        return self._default
    @default.setter
    def default(self, val):
        self._default = val
    @default.deleter
    def default(self):
        self._default = MISSING



class FunctionSpec:

    def __init__(self, name, params = None, body = None):
        _is_valid_python_name(name)
        self.name = name
        self._params = params
        self._body = body
    

    def build_func(self, namespace = None):
        if namespace is None:
            frame = inspect.currentframe().f_back
            namespace = frame.f_globals

        src = f"def {self.name}({', '.join(self._params)}):"
        src += "\n" + "\n".join(f"  {line}" for line in self._body.splitlines())
        
        if namespace is None:
            namespace = globals()
        exec(src, namespace)
        print(str(self))

        return namespace[self.name]
    
    def getbody(func):
        if func.__class__.__name__ == "function":
            return inspect.getsource(func)
        elif isinstance(FunctionSpec, func):
            return func._body
        else:
            raise ValueError(f"{func} must be of type function or FunctionSpec")
    
    def __str__(self):
        
        s = f"def {self.name}({', '.join(self._params)}):"
        s += "\n" + "\n".join(f"  {line}" for line in self._body.splitlines())
        return s


