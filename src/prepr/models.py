from . import types
import dataclasses


class CSHandler:
    """Used to create a colorspace handler given a valid `types.Colorspace` (e.g. those
    found in `Colorspace`).
    
    """
    def __init__(self, cs: types.Colorspace) -> None:
        self.cs = cs
    def f_function(self, __text) -> str:
        return self.cs.c_function + __text + self.cs.c_reset
    def f_class(self, __text) -> str:
        return self.cs.c_class + __text + self.cs.c_reset
    def f_string(self, __text) -> str:
        return self.cs.c_string + __text + self.cs.c_reset
    def f_number(self, __text) -> str:
        return self.cs.c_number + __text + self.cs.c_reset
    def f_other(self, __text) -> str:
        return self.cs.c_other + __text + self.cs.c_reset
    def f_variable(self, __text) -> str:
        return self.cs.c_variable + __text + self.cs.c_reset
    def f_attribute(self, __text) -> str:
        return self.cs.c_attribute + __text + self.cs.c_reset
    def f_argument(self, __text) -> str:
        return self.cs.c_argument + __text + self.cs.c_reset
    def f_operator(self, __text) -> str:
        return self.cs.c_operator + __text + self.cs.c_reset
    def f_comment(self, __text) -> str:
        return self.cs.c_comment + __text + self.cs.c_reset
    def f_bracket(self, __text) -> str:
        return self.cs.c_bracket + __text + self.cs.c_reset
    def f_error(self, __text) -> str:
        return self.cs.c_error + __text + self.cs.c_reset
    def f_boolean(self, __text) -> str:
        return self.cs.c_boolean + __text + self.cs.c_reset
    def f_enum(self, __text) -> str:
        return self.cs.c_enum + __text + self.cs.c_reset
    def f_reset(self, __text) -> str:
        return self.cs.c_reset + __text + self.cs.c_reset


class Colorspace:

    class rgbfull:
        """The most accurate of the colorspaces that uses full RGB.
        
        """
        c_function = "\033[38;2;219;219;170m"
        c_class = "\033[38;2;77;200;176m"
        c_string = "\033[38;2;205;144;120m"
        c_number = "\033[38;2;180;205;168m"
        c_other = "\033[38;2;211;211;211m"
        c_variable = "\033[38;2;156;219;253m"
        c_attribute = "\033[38;2;156;219;253m"
        c_argument = "\033[38;2;156;219;253m"
        c_operator = "\033[38;2;211;211;211m"
        c_comment = "\033[38;2;109;109;109m"
        c_bracket = "\033[38;2;254;214;24m"
        c_error = "\033[38;2;243;71;70m"
        c_boolean = "\033[38;2;86;156;213m"
        c_enum = "\033[38;2;80;193;253m"
        c_reset = "\033[0m"
    class rgb256:
        """Less accurate than `rgbfull` but has slightly greater compatability in other
        terminals.
        
        """
        c_function = "\033[38;5;179m"
        c_class = "\033[38;5;43m"
        c_string = "\033[38;5;180m"
        c_number = "\033[38;5;151m"
        c_other = "\033[38;5;251m"
        c_variable = "\033[38;5;153m"
        c_attribute = "\033[38;5;153m"
        c_argument = "\033[38;5;153m"
        c_operator = "\033[38;5;251m"
        c_comment = "\033[38;5;241m"
        c_bracket = "\033[38;5;221m"
        c_error = "\033[38;5;203m"
        c_boolean = "\033[38;5;26m"
        c_enum = "\033[38;5;26m"
        c_reset = "\033[0m"
    class rgb8:
        """The least accurate but most compatible colorspace. Works in almost all
        terminals.
        
        """
        c_function = "\033[33m"
        c_class = "\033[32m"
        c_string = "\033[31m"
        c_number = "\033[36m"
        c_other = "\033[37m"
        c_variable = "\033[36m"
        c_attribute = "\033[36m"
        c_argument = "\033[36m"
        c_operator = "\033[37m"
        c_comment = "\033[30m"
        c_bracket = "\033[33m"
        c_error = "\033[31m"
        c_boolean = "\033[34m"
        c_enum = "\033[34m"
        c_reset = "\033[0m"
    class none:
        """A colorspace that will apply no terminal formatting.
        
        """
        c_function = ""
        c_class = ""
        c_string = ""
        c_number = ""
        c_other = ""
        c_variable = ""
        c_attribute = ""
        c_argument = ""
        c_operator = ""
        c_comment = ""
        c_bracket = ""
        c_error = ""
        c_boolean = ""
        c_enum = ""
        c_reset = ""
    @dataclasses.dataclass
    class custom:
        """A custom colorspace.
        
        """
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


class settings:
    """Global settings used by all `prepr` instances. `csh` (colorspace handler) must be
    created with the `CSHandler` class and a valid `Colorspace`, e.g.
    `CSHandler(Colorspace.rgb256)`.
    
    """
    indent: str = "    "
    line_break: str = "\n"
    comma: str = ", "
    colon: str = ": "
    semicolon: str = "; "
    equals: str = " = "
    comment: str = " # "
    csh = CSHandler(Colorspace.rgbfull)
    force_lists_collapsed: bool = False
    force_tuples_collapsed: bool = False
    force_dicts_collapsed: bool = False
    @staticmethod
    def default() -> None:
        settings.indent = "    "
        settings.line_break = "\n"
        settings.comma = ", "
        settings.colon = ": "
        settings.semicolon = "; "
        settings.equals = " = "
        settings.comment = " # "
        settings.force_lists_collapsed = False
        settings.force_tuples_collapsed = False
        settings.force_dicts_collapsed = False
    @staticmethod
    def minimal() -> None:
        settings.indent = ""
        settings.line_break = ""
        settings.comma = ","
        settings.colon = ":"
        settings.semicolon = ";"
        settings.equals = "="
        settings.comment = "#"
        settings.force_lists_collapsed = True
        settings.force_tuples_collapsed = True
        settings.force_dicts_collapsed = True
    def update(
        self,
        indent: str = types.MISSING,
        line_break: str = types.MISSING,
        comma: str = types.MISSING,
        colon: str = types.MISSING,
        semicolon: str = types.MISSING,
        equals: str = types.MISSING,
        comment: str = types.MISSING,
        csh: CSHandler = types.MISSING,
        force_lists_collapsed: bool = types.MISSING,
        force_tuples_collapsed: bool = types.MISSING,
        force_dicts_collapsed: bool = types.MISSING
    ):
        """Batch-update settings.
        
        """
        pairs = [
            ("indent", indent),
            ("line_break", line_break),
            ("comma", comma),
            ("colon", colon),
            ("semicolon", semicolon),
            ("equals", equals),
            ("comment", comment),
            ("csh", csh),
            ("force_lists_collapsed", force_lists_collapsed),
            ("force_tuples_collapsed", force_tuples_collapsed),
            ("force_dicts_collapsed", force_dicts_collapsed)
        ]
        for name, value in pairs:
            if value != types.MISSING:
                setattr(self, name, value)


class prepr_str(str):
    """A `str` instance with an added `_prepr` attribute to store the `prepr`
    instance used to create it. Used for nested reprs.
    
    """
    def __new__(self, text, *args, **kwargs):
        return str.__new__(self, text)
    def __init__(self, text: str, _prepr: types.prepr):
        str.__init__(text)
        self._prepr = _prepr
