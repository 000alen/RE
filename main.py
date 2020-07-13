"""A very basic definition of BaseTypes using RE."""

from RE.RegularExpression.Literal import Literal
from RE.RegularExpression.One import One
from RE.RegularExpression.Optional import Optional
from RE.RegularExpression.Wildcard import Wildcard
from RE.RegularExpression.Zero import Zero

_sign = Literal("+") | Literal("-")
_digit = Literal("0") >> Literal("9")

base_types = {
    "integer": Optional(_sign) + One(_digit),
    "decimal": Optional(_sign) + Zero(_digit) + Literal(".") + One(_digit),
    "boolean": Literal("True") | Literal("False"),
    "undefined": Literal("Undefined"),
    "string": Literal("\"") + Zero(Wildcard()) + Literal("\""),
}

string = input("> ")
for name, expression in base_types.items():
    if expression.match(string):
        print(name)
