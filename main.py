from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import *
from RE.Utilities import show_finite_state_machine


expressions = [
    Optional(Literal("+"), Literal("-")) + 
    One(Literal("0") >> Literal("9")) +
    Literal(".") +
    Zero(Literal("0") >> Literal("9"))
]

string = input("> ")
for i, expression in enumerate(expressions):
    expression.compile()
    print(type(expression).__name__)
    print("blocks:", expression.blocks)
    print("inner_blocks:",expression.inner_blocks)

    print(expression.match(string))
    show_finite_state_machine(
        expression.finite_state_machine, "./debug/" + str(i) + ".png")
    print()
