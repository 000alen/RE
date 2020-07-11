from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import *
from RE.Utilities import show_finite_state_machine


expressions = [
    Literal("Hola") | Literal("Adios"),
    (Literal("Hola") | Literal("Adios")) + Literal("!"),
    (Literal("Hola") | Literal("Adios")) + One(Literal("!"))
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
