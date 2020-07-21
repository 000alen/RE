"""A very basic definition of BaseTypes using RE."""
from RE.RegularExpression.Literal import Literal
from RE.RegularExpression.One import One
from RE.RegularExpression.Optional import Optional

_sign = Literal("+") | Literal("-")
_digit = Literal("0") >> Literal("9")
_exponent = (Literal('e') | Literal("E")) + Optional(_sign) + One(_digit)

expression = Optional(_sign) + One(_digit) + Optional(_exponent)

while True:
    print(
        list(
            expression.search_all(
                input("> ")
            )
        )
    )
