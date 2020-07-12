from json import dump, load

from pygraphviz import AGraph

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import RegularExpression


def show_finite_state_machine(finite_state_machine: FiniteStateMachine, name: str):
    G = AGraph(strict=False, directed=True)
    G.add_nodes_from(finite_state_machine.state_set)
    for initial_state in finite_state_machine.initial_states:
        G.get_node(initial_state).attr["color"] = "green"
    for element, connections in finite_state_machine.transitions.items():
        for from_state, to_states in connections.items():
            for to_state in to_states:
                G.add_edge(from_state, to_state, element,
                           label=element, fontsize=18)
    for final_state in finite_state_machine.final_states:
        G.get_node(final_state).attr["color"] = "red"
    G.draw(name, prog="dot")


def export_finite_state_machine(finite_state_machine: FiniteStateMachine, name: str):
    data = {
        element: {
            int(from_state): list(to_states)
            for from_state, to_states in connections.items()
        }
        for element, connections in finite_state_machine.transitions.items()
    }
    data.update(
        {
            "initial_states": list(finite_state_machine.initial_states),
            "final_states": list(finite_state_machine.final_states),
            "default_states": list(finite_state_machine.default_states)
        }
    )
    dump(data, open(name, "w"))


def import_finite_state_machine(name: str):
    data: dict = load(open(name, "r"))
    initial_states = set(data.pop("initial_states"))
    final_states = set(data.pop("final_states"))
    default_states = set(data.pop("default_states"))
    transitions = {
        element: {
            int(from_state): set(to_states)
            for from_state, to_states in connections.items()
        }
        for element, connections in data.items()
    }
    finite_state_machine = FiniteStateMachine(initial_states, final_states, default_states)
    finite_state_machine.transitions = transitions
    return finite_state_machine
