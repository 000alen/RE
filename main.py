from RE.RegularExpression import *

a = Literal("gr") + Optional(Literal("a"), Literal("e")) + Literal("y!")
print(a)
