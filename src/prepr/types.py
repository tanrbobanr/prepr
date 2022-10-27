from __future__ import annotations
import typing


class MISSING:
    """A type to indicate no value in `prepr.kwarg`.
    
    """


class prepr_str(str):
    def __new__(self, text, *args, **kwargs): ...
    def __init__(self, text: str, _prepr: prepr): ...


class Self:
    """Used to indicate a self in the representation.
    
    """


class prepr:
    def __init__(self, inst, variable_name: str = None, note: str = None) -> None: ...
    def arg(self, v) -> prepr: ...
    def args(self, *v) -> prepr: ...
    def kwarg(self, k, v, d: typing.Any = MISSING) -> prepr: ...
    def kwargs(self, d: typing.Any = MISSING, **kv) -> prepr: ...
    def attr(self, k, v, d: typing.Any = MISSING) -> prepr: ...
    def attrs(self, d: typing.Any = MISSING, **kv) -> prepr: ...
    def _preformat_args(self, indent: str, line_break: str) -> str: ...
    def _preformat_attrs(self, custom_line_break: str) -> str: ...
    def _build_collapsed(self) -> prepr_str: ...
    def _build_simple(self, indent: str, line_break: str) -> prepr_str: ...
    def build(self, simple: bool = False, collapsed: bool = False) -> prepr_str: ...


class Colorspace:
    c_function: str
    c_class: str
    c_string: str
    c_number: str
    c_other: str
    c_variable: str
    c_attribute: str
    c_argument: str
    c_operator: str
    c_comment: str
    c_bracket: str
    c_error: str
    c_boolean: str
    c_enum: str
    c_reset: str
