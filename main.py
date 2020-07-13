from RE.RegularExpression.Literal import Literal

expression = Literal(", ")
string = input("> ")
print(expression.split(string))
