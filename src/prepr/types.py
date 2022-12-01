import typing


class MISSING:
    """A type to indicate no value in `prepr.kwarg`.
    
    """


class pstr(str):
    _prepr: "prepr"
    def __new__(self, text, *args, **kwargs): ...
    def __init__(self, text: str, _prepr: "prepr"): ...


class prepr:
    def __init__(self, inst, variable_name: str = None,
                 note: str = None) -> None: ...
    def arg(self, v) -> "prepr": ...
    def args(self, *v) -> "prepr": ...
    def kwarg(self, k, v, d: typing.Any = MISSING) -> "prepr": ...
    def kwargs(self, d: typing.Any = MISSING, **kv) -> "prepr": ...
    def attr(self, k, v, d: typing.Any = MISSING) -> "prepr": ...
    def attrs(self, d: typing.Any = MISSING, **kv) -> "prepr": ...
    def _format_args(self, exc: typing.Dict[int, str], i: str,
                     lb: str) -> str: ...
    def _format_attrs(self, exc: typing.Dict[int, str], lb: str) -> str: ...
    def _build_collapsed(self) -> pstr: ...
    def _build_simple(self, exc: typing.Dict[int, str], i: str,
                      lb: str) -> str: ...
    def build(self, simple: bool = False, collapsed: bool = False,
              return_prepr: bool = False) -> "typing.Union[pstr, prepr]": ...


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
