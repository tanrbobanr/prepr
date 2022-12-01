from . import types, models
import textwrap
import inspect
import enum
import typing
import types as builtin_types


def concat(*__text: str) -> str:
    """Concatenate any number of `str` objects together.
    
    """
    return "".join(__text)


def attempt_str(value) -> str:
    """Attempt to run `str(__value)`. If an error is encountered, return "???"
    (formatted as error).

    """
    try:
        return str(value)
    except Exception:
        return concat(
            models.settings.csh.f_operator(".").join(
                [models.settings.csh.f_class(class_name) for class_name
                in type(value).__qualname__.split(".")]),
            models.settings.csh.f_bracket("("),
            models.settings.csh.f_error("!!!"),
            models.settings.csh.f_bracket(")"))


def indent(__str: str, __indent: str) -> str:
    """Increases the indent of each line in `__str` by `__indent`.
    
    """
    return textwrap.indent(__str, __indent)


def format_str(v: str) -> str:
    """Format a string value.
    
    """
    return models.settings.csh.f_string(concat("\"",
        v.replace("\\", "\\\\").replace("\"", "\\\""), "\""))

def format_num(v: typing.Union[int, float]) -> str:
    """Format a number (int/float) value.
    
    """
    return models.settings.csh.f_number(attempt_str(v))

def format_bool_none(v: typing.Union[bool, None]) -> str:
    """Format boolean or None value.
    
    """
    return models.settings.csh.f_boolean(attempt_str(v))

def format_list(v: list, exc: typing.Dict[int, str], i: str, lb: str) -> str:
    """Format a list value.
    
    """
    I = "" if models.settings.force_lists_collapsed else i
    LB = "" if models.settings.force_lists_collapsed else lb
    values = [concat(LB, format_value(V, exc, I, LB)) for V in v]
    return concat(
        models.settings.csh.f_bracket("["),
        indent(
            models.settings.csh.f_operator(models.settings.comma).join(values),
            I
        ),
        LB,
        models.settings.csh.f_bracket("]")
    )

def format_tuple(v: tuple, exc: typing.Dict[int, str], i: str, lb: str) -> str:
    """Format a tuple value.
    
    """
    I = "" if models.settings.force_tuples_collapsed else i
    LB = "" if models.settings.force_tuples_collapsed else lb
    values = [concat(LB, format_value(V, exc, I, LB)) for V in v]
    return concat(
        models.settings.csh.f_bracket("("),
        indent(
            models.settings.csh.f_operator(models.settings.comma).join(values),
            I
        ),
        (models.settings.csh.f_operator(models.settings.comma)
         if len(values) == 1 else ""),
        LB,
        models.settings.csh.f_bracket(")")
    )

def format_dict(v: dict, exc: typing.Dict[int, str], i: str, lb: str) -> str:
    """Format a dict value.
    
    """
    I = "" if models.settings.force_dicts_collapsed else i
    LB = "" if models.settings.force_dicts_collapsed else lb
    values = [concat(LB, format_value(k, exc, I, LB),
              models.settings.csh.f_operator(models.settings.colon),
              format_value(V, exc, I, LB)) for k, V in v.items()]
    return concat(
        models.settings.csh.f_bracket("{"),
        indent(
            models.settings.csh.f_operator(models.settings.comma).join(values),
            I),
        LB,
        models.settings.csh.f_bracket("}")
    )

def format_class(v: object) -> str:
    """Format a class (not instance) value.
    
    """
    return models.settings.csh.f_operator(".").join([
        models.settings.csh.f_class(class_name) for class_name
        in v.__qualname__.split(".")])

def format_func(v, lb: str) -> str:
    """Format a function value.
    
    """
    if "__wrapped__" in dir(v):
        wrapped = True
    else:
        wrapped = False
    quals: list[str] = v.__qualname__.split(".")
    quals_formatted = [models.settings.csh.f_class(q) for q in quals[:-1]] + [
        models.settings.csh.f_function(quals[-1])]
    QUAL = models.settings.csh.f_operator(".").join(quals_formatted)
    if wrapped and "\n" in lb:
        return QUAL + models.settings.csh.f_comment(models.settings.comment +
            "wrapped")
    return QUAL

def format_enum(v: enum.Enum) -> str:
    """Format a `enum.Enum` value.
    
    """
    values = str(v).split(".")
    return concat(
        models.settings.csh.f_operator(".").join([
            models.settings.csh.f_class(class_name)
            for class_name in values[:-1]]),
        models.settings.csh.f_operator("."),
        models.settings.csh.f_enum(values[-1]))


def format_prepr(v: types.prepr, exc: typing.Dict[int, str], i: str,
                 lb: str) -> str:
    """Format a `prepr` value.
    
    """
    if id(v._inst) in exc:
        return models.settings.csh.f_error(v._variable)
    I = "" if models.settings.force_sub_preprs_collapsed else i
    LB = "" if models.settings.force_sub_preprs_collapsed else lb
    return v._build_simple(exc, I, LB)


def format_value(v, exc: typing.Dict[int, str], i: str, lb: str) -> str:
    """Format a given text value with the global colorspace depending on its
    type.
    
    """
    TYPE = type(v)
    if TYPE == str:
        return format_str(v)
    if TYPE in [int, float]:
        return format_num(v)
    if TYPE == bool or v is None:
        return format_bool_none(v)
    if TYPE == list:
        return format_list(v, exc, i, lb)
    if TYPE == tuple:
        return format_tuple(v, exc, i, lb)
    if TYPE == dict:
        return format_dict(v, exc, i, lb)
    if inspect.isclass(v):
        return format_class(v)
    if TYPE in [builtin_types.FunctionType, builtin_types.BuiltinFunctionType,
                builtin_types.BuiltinMethodType]:
        return format_func(v, lb)
    if isinstance(v, enum.Enum):
        return format_enum(v)
    if isinstance(v, types.pstr):
        return format_prepr(v._prepr, exc, i, lb)
    if hasattr(v, "__repr__"):
        try:
            _prepr = v.__repr__(return_prepr=True)
        except Exception:
            _prepr = None
        if isinstance(_prepr, types.prepr):
            return format_prepr(_prepr, exc, i, lb)
    if hasattr(v, "__str__"):
        try:
            _prepr = v.__str__(return_prepr=True)
        except Exception:
            _prepr = None
        if isinstance(_prepr, types.prepr):
            return format_prepr(_prepr, exc, i, lb)
    return models.settings.csh.f_other(attempt_str(v))
