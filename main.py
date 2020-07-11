from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import *
from RE.Utilities import show_finite_state_machine


expressions = [
    (Literal("Hola") | Literal("Adios")) + One(Literal("!"))
]

string = input("> ")
for i, expression in enumerate(expressions):
    expression.compile()
    print(expression.match(string))
    show_finite_state_machine(
        expression.finite_state_machine, "./debug/" + str(i) + ".png")
