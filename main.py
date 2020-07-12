from RE.RegularExpression.Literal import Literal
from RE.RegularExpression.Choose import Choose

expression = Choose(Literal("0"), Literal("1"))
expression.compile()
expression.match("0")
