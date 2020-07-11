from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import *
from RE.Utilities import show_finite_state_machine

expressions = [
    Choose(Literal("+"), Literal("-")) +
    One(Literal("0") >> Literal("9")) +
    Literal(".") +
    Zero(Literal("0") >> Literal("9"))
]

string = input("> ")
for i, expression in enumerate(expressions):
    expression.compile()

    print(expression.finite_state_machine.get_state(0))
    print(expression.match(string))
    show_finite_state_machine(
        expression.finite_state_machine, "./debug/" + str(i) + ".png")
