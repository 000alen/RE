from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import *
from RE.Utilities import show_finite_state_machine, export_finite_state_machine, import_finite_state_machine

finite_state_machine = import_finite_state_machine("./debug/0.json")
show_finite_state_machine(finite_state_machine, "./debug/0.png")

print(finite_state_machine.accepts(input("> ")))
