import pygraphviz as pgv

from RE.FiniteStateMachine import FiniteStateMachine


def show_finite_state_machine(finite_state_machine: FiniteStateMachine, name: str = "FSM.png"):
    G = pgv.AGraph(strict=False, directed=True)
    G.add_nodes_from(finite_state_machine.state_set)
    for element, connections in finite_state_machine.transitions.items():
        for from_state, to_states in connections.items():
            for to_state in to_states:
                G.add_edge(from_state, to_state, element, label=element)
    G.draw(name, prog="dot")
