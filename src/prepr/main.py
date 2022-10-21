from __future__ import annotations
import textwrap, inspect, typing, types
from .models import settings, prepr_str
from . import types as prepr_types


def _attempt_str(value) -> str:
    """Attempt to run `str(__value)`. If an error is encountered, return "???"
    (formatted as error).

    """
    try:
        return str(value)
    except Exception:
        return _concat(
            settings.csh.f_operator(".").join([settings.csh.f_class(class_name) for class_name in type(value).__qualname__.split(".")]),
            settings.csh.f_bracket("("),
            settings.csh.f_error("!!!"),
            settings.csh.f_bracket(")")
        )


def _is_self(parent, value) -> bool:
    if id(parent) == id(value):
        return True
    return False


def _indent(__str: str, __indent: str) -> str:
    """Increases the indent of each line in `__str` by `__indent`.
    
    """
    return textwrap.indent(__str, __indent)


def _format_value(value, indent: str, line_break: str) -> str:
    """Format a given text value with the global colorspace depending on its type.
    
    """
    # defining the type of value so we don't have to call type(value) a bunch of times
    _type = type(value)

    # if value is self
    if value == prepr_types.Self:
        return settings.csh.f_boolean("Self")

    # if value is a str
    if _type == str:
        return settings.csh.f_string(_concat("\"", value.replace("\\", "\\\\").replace("\"", "\\\""), "\""))
    
    # if value is a number
    if _type in [int, float]:
        return settings.csh.f_number(_attempt_str(value))
    
    # if value is a bool
    if _type == bool:
        return settings.csh.f_boolean(_attempt_str(value))

    # if value is a list
    if _type == list:
        i = "" if settings.force_lists_collapsed else indent
        lb = "" if settings.force_lists_collapsed else line_break
        values = [_concat(lb, _format_value(v, i, lb)) for v in value]
        return _concat(
            settings.csh.f_bracket("["),
            _indent(settings.csh.f_operator(settings.comma).join(values), i),
            lb,
            settings.csh.f_bracket("]")
        )

    # if value is a tuple
    if _type == tuple:
        i = "" if settings.force_tuples_collapsed else indent
        lb = "" if settings.force_tuples_collapsed else line_break
        values = [_concat(lb, _format_value(v, i, lb)) for v in value]
        return _concat(
            settings.csh.f_bracket("("),
            _indent(settings.csh.f_operator(settings.comma).join(values), i),
            settings.csh.f_operator(settings.comma) if len(values) == 1 else "",
            lb,
            settings.csh.f_bracket(")")
        )
    
    # if value is a dict
    if _type == dict:
        i = "" if settings.force_dicts_collapsed else indent
        lb = "" if settings.force_dicts_collapsed else line_break
        values = [_concat(lb, _format_value(k, i, lb), settings.csh.f_operator(settings.colon), _format_value(v, i, lb)) for k, v in value.items()]
        return _concat(
            settings.csh.f_bracket("{"),
            _indent(settings.csh.f_operator(settings.comma).join(values), i),
            lb,
            settings.csh.f_bracket("}")
        )

    # if value is a class (not a class instance)
    if inspect.isclass(value):
        return settings.csh.f_operator(".").join([settings.csh.f_class(class_name) for class_name in value.__qualname__.split(".")])

    # if value is a function
    if _type in [types.FunctionType, types.BuiltinFunctionType, types.BuiltinMethodType]:
        if "__wrapped__" in dir(value):
            wrapped = True
        else:
            wrapped = False
        quals = value.__qualname__.split(".")
        quals_formatted = [settings.csh.f_class(q) for q in quals[:-1]] + [settings.csh.f_function(quals[-1])]
        qual_formatted = settings.csh.f_operator(".").join(quals_formatted)
        if wrapped and "\n" in line_break:
            qual_formatted += settings.csh.f_comment(settings.comment + "wrapped")
        return qual_formatted
    
    # if value is already a prepr_str
    if isinstance(value, prepr_str):
        _prepr = value._prepr
        simple = _prepr._build_simple(indent, line_break)
        return simple

    # if value has a __repr__ method defined and the return of that method is a prepr_str
    if hasattr(value, "__repr__"):
        # catch an error since this could be a user-defined method
        try:
            _repr = value.__repr__()
        except Exception:
            _repr = None
        if isinstance(_repr, prepr_str):
            _prepr = _repr._prepr
            simple = _prepr._build_simple(indent, line_break)
            return simple
    
    # if value has an __str__ method defined and the return of that method is a prepr_str
    if hasattr(value, "__str__"):
        # catch an error since this could be a user-defined method
        try:
            _str = value.__str__()
        except Exception:
            _str = None
        if isinstance(_str, prepr_str):
            _prepr = _str._prepr
            simple = _prepr._build_simple(indent, line_break)
            return simple
    
    # all other cases
    return settings.csh.f_other(_attempt_str(value))


def _concat(*__text: str) -> str:
    """Concatenate any number of `str` objects together.
    
    """
    return "".join(__text)


class prepr:
    def __init__(self, inst, variable_name: str = None, note: str = None) -> None:
        """Create a pretty-formatted string for class representations.
        
        Parameters
        ----------
        inst : any
            The class instance being represented.
        variable_name : str, optional
            The name of the variable that the representation will be assigned to when
            printed.
        note : str, optional
            A comment about the class.
        
        Example usage
        -------------
        ```
        class example_class:
            def __init__(self, a, b, c = None):
                self.a = a
                self.b = b
                self.c = c
                # a value which will be set
                # somewhere down the line:
                self.something_else = None
            def __repr__(self):
                R = prepr(self)
                R.args(self.a, self.b)
                R.kwarg("c", self.c)
                R.attr(self.something_else)
                return R.build()
        ```

        """
        self._exc = None
        try:
            self._inst = inst
            self._variable: str = settings.csh.f_variable(variable_name or "__" + type(inst).__name__.lower() + "__")
            self._note: str = settings.csh.f_comment(settings.comment + note if note else "")
            self._name: str = settings.csh.f_class(type(inst).__name__)
            self._args: list[str] = []
            self._kwargs: dict[str, str] = {}
            self._attrs: dict[str, str] = {}
        except Exception as exc:
            self._exc = exc
    

    def arg(self, v) -> prepr:
        """Add a positional argument.
        
        """
        if not self._exc:
            try:
                if _is_self(self._inst, v):
                    self._args.append(prepr_types.Self)
                    return self
                self._args.append(v)
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def args(self, *v) -> prepr:
        """Convenience method for adding multiple arguments in one function call.
        
        """
        if not self._exc:
            try:
                self._args.extend([prepr_types.Self if _is_self(self._inst, j) else j for j in v])
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def kwarg(self, k, v, d: typing.Any = prepr_types.MISSING) -> prepr:
        """Add a keyword argument.

        `d` is optional and can be set to any value. If `v` (the value) is equal to `d`
        (the default value), it will be ommited from the representation.
        
        """
        if not self._exc:
            try:
                if (d != prepr_types.MISSING and d == v) or _is_self(self._inst, v):
                    self._kwargs[k] = prepr_types.Self
                    return self
                self._kwargs[k] = v
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def kwargs(self, d: typing.Any = prepr_types.MISSING, **kv) -> prepr:
        """Convenience method for adding multiple keyword arguments in one function call.

        `d` is optional and can be set to any value. If and value in `kv` is equal to `d`
        (the default value), the pair will be ommited from the representation.
        
        """
        if not self._exc:
            try:
                temp = {}
                if d != prepr_types.MISSING:
                    for k, v in kv.items():
                        if v == d or _is_self(self._inst, v):
                            continue
                        temp[k] = v
                else:
                    for k, v in kv.items():
                        if _is_self(self._inst, v):
                            temp[k] = prepr_types.Self
                            continue
                        temp[k] = v
                self._kwargs.update(temp)
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self


    def attr(self, k, v, d: typing.Any = prepr_types.MISSING) -> prepr:
        """Add an attribute.

        This should only be used for variable attributes that change sometime after
        class initialization.

        `d` is optional and can be set to any value. If `v` (the value) is equal to `d`
        (the default value), it will be ommited from the representation.
        
        """
        if not self._exc:
            try:
                if (d != prepr_types.MISSING and d == v) or _is_self(self._inst, v):
                    self._attrs[k] = prepr_types.Self
                    return self
                self._attrs[k] = v
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def attrs(self, d: typing.Any = prepr_types.MISSING, **kv) -> prepr:
        """Convenience method for adding multiple attributes in one function call.

        `d` is optional and can be set to any value. If and value in `kv` is equal to `d`,
        the pair will be ommited from the representation.
        
        """
        if not self._exc:
            try:
                temp = {}
                if d != prepr_types.MISSING:
                    for k, v in kv.items():
                        if v == d or _is_self(self._inst, v):
                            continue
                        temp[k] = v
                else:
                    for k, v in kv.items():
                        if _is_self(self._inst, v):
                            temp[k] = prepr_types.Self
                            continue
                        temp[k] = v
                self._attrs.update(temp)
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def _preformat_args(self, indent: str, line_break: str) -> str:
        """Format the positional and keyword arguments.
        
        """
        formatted_args = [_concat(indent, line_break, _format_value(v, indent, line_break)) for v in self._args]
        formatted_kwargs = [_concat(indent, line_break, settings.csh.f_argument(_attempt_str(k)), settings.csh.f_operator(settings.equals), _format_value(v, indent, line_break)) for k, v, in self._kwargs.items()]
        return _indent(
            settings.csh.f_operator(settings.comma).join(formatted_args + formatted_kwargs),
            indent
        ) if formatted_args or formatted_kwargs else ""
    

    def _preformat_attrs(self, custom_line_break: str) -> str:
        """Format the attributes.
        
        """
        formatted_attrs = [_concat(self._variable, settings.csh.f_operator("."), settings.csh.f_attribute(k), settings.csh.f_operator(settings.equals), _format_value(v, settings.indent, settings.line_break)) for k, v in self._attrs.items()]
        return custom_line_break.join(formatted_attrs)


    def _build_collapsed(self) -> prepr_str:
        """Return `<name>(...)`.
        
        """
        return prepr_str(
            _concat(
                self._name,
                settings.csh.f_bracket("("),
                settings.csh.f_operator("..."),
                settings.csh.f_bracket(")")
            ),
            self
        )


    def _build_simple(self, indent: str, line_break: str) -> prepr_str:
        """Create the main representation without any attributes or variable name.
        
        """
        preformatted_args = self._preformat_args(indent, line_break)
        return prepr_str(
            _concat(
                self._name,
                settings.csh.f_bracket("("),
                self._note if "\n" in settings.line_break else "",
                preformatted_args,
                indent if self._preformat_args(indent, line_break) else "",
                line_break if self._preformat_args(indent, line_break) else "",
                settings.csh.f_bracket(")")
            ),
            self
        )
    
    
    def build(self, simple: bool = False, collapsed: bool = False) -> prepr_str:
        """Build the representation.
        
        Arguments
        ---------
        simple : bool, optional, default=False
            If True, the attributes and variable name will be ommitted.
        collapsed : bool, optional, default=False
            If True, only the class name will be included with parentheses and an
            ellipsis (for example, `ExampleClass(...)`). Takes precedence over `simple`.

        """
        if not self._exc:
            try:
                if collapsed is True:
                    return self._build_collapsed()

                # create the simple representation now as it
                # used whether or not `simple` is True or False
                simple_repr = self._build_simple(settings.indent, settings.line_break)

                # if `simple` is True, the simply return simple_repr
                if simple is True:
                    return simple_repr
                
                # create the line break used to separate the
                # simple_repr and each attribute assignment
                lb = _concat(
                    settings.csh.f_error(settings.semicolon),
                    settings.indent,
                    settings.line_break
                )

                # return the full repr
                return prepr_str(
                    _concat(
                        self._variable,
                        settings.csh.f_operator(settings.equals),
                        simple_repr,
                        (lb + self._preformat_attrs(lb) if self._attrs else "")
                    ),
                    self
                )
            except Exception as exc:
                self._exc = exc
        return prepr_str("\033[32mPreprBuildFailure" + "\033[33m(" + "\033[31m\"" + str(self._exc) + "\"" + "\033[33m)\033[0m", self)
