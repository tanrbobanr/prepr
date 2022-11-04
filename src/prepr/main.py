import typing
from . import types, utils, models


class prepr(types.prepr):
    def __init__(self, inst, variable_name: str = None,
                 note: str = None) -> None:
        """Create a pretty-formatted string for class representations.
        
        Parameters
        ----------
        inst : any
            The class instance being represented.
        variable_name : str, optional
            The name of the variable that the representation will be assigned to
            when printed.
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
            self._variable: str = models.settings.csh.f_variable(variable_name
                or "__" + type(inst).__name__.lower() + "__")
            self._note: str = models.settings.csh.f_comment(
                models.settings.comment + note if note else "")
            self._name: str = models.settings.csh.f_class(type(inst).__name__)
            self._args: list[str] = []
            self._kwargs: dict[str, str] = {}
            self._attrs: dict[str, str] = {}
        except Exception as exc:
            self._exc = exc
    

    def arg(self, v) -> types.prepr:
        """Add a positional argument.
        
        """
        if not self._exc:
            try:
                self._args.append(v)
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def args(self, *v) -> types.prepr:
        """Convenience method for adding multiple arguments in one function
        call.
        
        """
        if not self._exc:
            try:
                self._args.extend(v)
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def kwarg(self, k, v, d: typing.Any = types.MISSING) -> types.prepr:
        """Add a keyword argument.

        `d` is optional and can be set to any value. If `v` (the value) is equal
        to `d` (the default value), it will be ommited from the representation.
        
        """
        if not self._exc:
            try:
                if (d != types.MISSING and d == v):
                    return self
                self._kwargs[k] = v
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def kwargs(self, d: typing.Any = types.MISSING, **kv) -> types.prepr:
        """Convenience method for adding multiple keyword arguments in one
        function call.

        `d` is optional and can be set to any value. If and value in `kv` is
        equal to `d` (the default value), the pair will be ommited from the
        representation.
        
        """
        if not self._exc:
            try:
                if d != types.MISSING:
                    temp = {}
                    for k, v in kv.items():
                        if v == d:
                            continue
                        temp[k] = v
                else:
                    self._kwargs.update(kv)
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self


    def attr(self, k, v, d: typing.Any = types.MISSING) -> types.prepr:
        """Add an attribute.

        This should only be used for variable attributes that change sometime
        after class initialization.

        `d` is optional and can be set to any value. If `v` (the value) is equal
        to `d` (the default value), it will be ommited from the representation.
        
        """
        if not self._exc:
            try:
                if d != types.MISSING and d == v:
                    return self
                self._attrs[k] = v
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def attrs(self, d: typing.Any = types.MISSING, **kv) -> types.prepr:
        """Convenience method for adding multiple attributes in one function
        call.

        `d` is optional and can be set to any value. If and value in `kv` is
        equal to `d`, the pair will be ommited from the representation.
        
        """
        if not self._exc:
            try:
                if d != types.MISSING:
                    temp = {}
                    for k, v in kv.items():
                        if v == d:
                            continue
                        temp[k] = v
                else:
                    self._attrs.update(kv)
                return self
            except Exception as exc:
                self._exc = exc
                return self
        return self
    

    def _format_args(self, exc: dict[int, str], i: str, lb: str) -> str:
        """Format the positional and keyword arguments.
        
        """
        formatted_args = [utils.concat(i, lb, utils.format_value(v, exc, i, lb))
                          for v in self._args]
        formatted_kwargs = [utils.concat(i, lb, 
            models.settings.csh.f_argument(k),
            models.settings.csh.f_operator(models.settings.equals),
            utils.format_value(v, exc, i, lb)) for k, v, in
            self._kwargs.items()]
        return utils.indent(models.settings.csh.f_operator(
            models.settings.comma).join(formatted_args + formatted_kwargs), i
            ) if formatted_args or formatted_kwargs else ""
    

    def _format_attrs(self, exc: dict[int, str], lb: str) -> str:
        """Format the attributes.
        
        """
        formatted_attrs = [utils.concat(
            self._variable,
            models.settings.csh.f_operator("."),
            models.settings.csh.f_attribute(k),
            models.settings.csh.f_operator(models.settings.equals),
            utils.format_value(
                v,
                exc,
                models.settings.indent,
                models.settings.line_break
            )
        ) for k, v in self._attrs.items()]
        return lb.join(formatted_attrs)


    def _build_collapsed(self) -> types.pstr:
        """Return `<name>(...)`.
        
        """
        return (
            utils.concat(
                self._name,
                models.settings.csh.f_bracket("("),
                models.settings.csh.f_operator("..."),
                models.settings.csh.f_bracket(")")
            ),
            self
        )


    def _build_simple(self, exc: dict[int, str], i: str, lb: str) -> str:
        """Create the main representation without any attributes or variable
        name.
        
        """
        args = self._format_args(exc, i, lb)
        return utils.concat(
            self._name,
            models.settings.csh.f_bracket("("),
            self._note if "\n" in models.settings.line_break else "",
            args,
            i if args else "",
            lb if args else "",
            models.settings.csh.f_bracket(")")
        )
    
    
    def build(self, simple: bool = False, collapsed: bool = False,
              return_prepr: bool = False) -> types.pstr | types.prepr:
        """Build the representation.
        
        Arguments
        ---------
        simple : bool, optional, default=False
            If True, the attributes and variable name will be ommitted.
        collapsed : bool, optional, default=False
            If True, only the class name will be included with parentheses and
            an ellipsis (for example, `ExampleClass(...)`). Takes precedence
            over `simple`.
        return_prepr : bool, optional, default=False
            A value used internally to resolve issues with recursion. Should not
            be defined by the user.

        """
        if not self._exc:
            try:
                if return_prepr:
                    return self
                if collapsed is True:
                    return self._build_collapsed()

                # create the simple representation now as it
                # used whether or not `simple` is True or False
                instance_exceptions = {id(self._inst): self._variable}
                simple_repr = self._build_simple(
                    instance_exceptions,
                    models.settings.indent,
                    models.settings.line_break
                )

                # if `simple` is True, the simply return simple_repr
                if simple is True:
                    return models.pstr(simple_repr, self)
                
                # create the line break used to separate the
                # simple_repr and each attribute assignment
                lb = utils.concat(
                    models.settings.csh.f_error(models.settings.semicolon),
                    models.settings.indent,
                    models.settings.line_break
                )

                # return the full repr
                return models.pstr(
                    utils.concat(
                        self._variable,
                        models.settings.csh.f_operator(models.settings.equals),
                        simple_repr,
                        (lb + self._format_attrs(instance_exceptions, lb) if
                         self._attrs else "")
                    ),
                    self
                )
            except Exception as exc:
                self._exc = exc
        return models.pstr("\033[32mPreprBuildFailure\033[33m(\033[31m\"" +
                           str(self._exc) + "\"\033[33m)\033[0m", self)
