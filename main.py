from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import *
from RE.Utilities import show_finite_state_machine, export_finite_state_machine, import_finite_state_machine

expression = Literal("\"") + Zero(Wildcard()) + Literal("\"")
expression.compile()
show_finite_state_machine(expression.finite_state_machine, "./debug/0.png")

print(expression.match(input("> ")))
