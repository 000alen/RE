"""A very basic definition of BaseTypes using RE."""

from RE.RegularExpression.Literal import Literal
from RE.RegularExpression.One import One
from RE.RegularExpression.Optional import Optional
from RE.RegularExpression.Wildcard import Wildcard
from RE.RegularExpression.Zero import Zero

_sign = Literal("+") | Literal("-")
_digit = Literal("0") >> Literal("9")
_exponent = (Literal('e') | Literal("E")) + Optional(_sign) + One(_digit)

expressions = {
    "integer": Optional(_sign) + One(_digit) + Optional(_exponent),
    "decimal": Optional(_sign) + Zero(_digit) + Literal(".") + One(_digit) + Optional(_exponent),
    "boolean": Literal("True") | Literal("False"),
    "undefined": Literal("Undefined"),
    "string": Literal("\"") + Zero(Wildcard()) + Literal("\""),
    "whitespace": One(Literal(" "))
}

for name, expression in expressions.items():
    expression.compile()
    for element, current_states in expression.finite_state_machine.run(input(name + "> ")):
        print(element, current_states)
