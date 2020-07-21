from RE.FiniteStateMachine import FiniteStateMachine

__all__ = (
    "draw_finite_state_machine",
    "export_finite_state_machine",
    "import_finite_state_machine"
)


def draw_finite_state_machine(finite_state_machine: FiniteStateMachine, path: str):
    """Creates a directed non-strict multi graph image representation of the FSM."""
    from pygraphviz import AGraph
    graph = AGraph(strict=False, directed=True)
    graph.add_nodes_from(finite_state_machine.state_set)
    for initial_state in finite_state_machine.initial_states:
        graph.get_node(initial_state).attr["color"] = "green"
    for element, transitions in finite_state_machine.transitions.items():
        for from_state, to_states in transitions.items():
            for to_state in to_states:
                graph.add_edge(from_state, to_state,
                               label=element)
    for final_state in finite_state_machine.final_states:
        graph.get_node(final_state).attr["color"] = "red"
    graph.draw(path, prog="dot")


def export_finite_state_machine(finite_state_machine: FiniteStateMachine, path: str):
    """Exports a json representation of a FSM."""
    from json import dump
    data = {}
    for element, connections in finite_state_machine.transitions.items():
        element = tuple(element) if type(element) is frozenset else element
        data[element] = {}
        for from_state, to_states in connections.items():
            data[element][from_state] = tuple(to_states)
    data.update(
        initial_states=tuple(finite_state_machine.initial_states),
        final_states=tuple(finite_state_machine.final_states),
    )
    dump(data, open(path, "w"))


def import_finite_state_machine(path: str) -> FiniteStateMachine:
    """Imports a json representation of a FSM."""
    from json import load
    data = load(open(path, "r"))
    initial_states = set(data.pop("initial_states"))
    final_states = set(data.pop("final_states"))
    transitions = {}
    for element, connections in data.items():
        element = frozenset(element) if type(element) is tuple else element
        transitions[element] = {}
        for from_state, to_states in connections.items():
            transitions[element][int(from_state)] = set(to_states)
    finite_state_machine = FiniteStateMachine(initial_states, final_states)
    finite_state_machine.transitions = transitions
    return finite_state_machine
