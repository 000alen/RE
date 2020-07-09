from RE.RegularExpression import Literal, Optional, Zero, One


binary = Literal("0") + Optional(Literal("b"), Literal("B")) + One(Optional(Literal("0"), Literal("1")))

# binary = Literal("0") + (Literal("b") or Literal("B")) + One(Literal("0") or Literal("1"))


print(binary.match(input(">>> ")))