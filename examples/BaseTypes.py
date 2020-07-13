"""A very basic definition of BaseTypes using RE."""

from RE.Lexer import Lexer
from RE.RegularExpression.Literal import Literal
from RE.RegularExpression.One import One
from RE.RegularExpression.Optional import Optional
from RE.RegularExpression.Wildcard import Wildcard
from RE.RegularExpression.Zero import Zero

_sign = Literal("+") | Literal("-")
_digit = Literal("0") >> Literal("9")
_exponent = (Literal('e') | Literal("E")) + Optional(_sign) + One(_digit)

base_type = {
    "integer": Optional(_sign) + One(_digit) + Optional(_exponent),
    "decimal": Optional(_sign) + Zero(_digit) + Literal(".") + One(_digit) + Optional(_exponent),
    "boolean": Literal("True") | Literal("False"),
    "undefined": Literal("Undefined"),
    "string": Literal("\"") + Zero(Wildcard()) + Literal("\""),
    "whitespace": One(Literal(" "))
}

lexer = Lexer(**base_type)
for i, token in lexer.lex(input("> ")):
    print(i, token)
