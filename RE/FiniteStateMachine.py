from typing import Dict, Generic, Iterator, Sequence, Set, Tuple, TypeVar

__all__ = (
    "EPSILON",
    "SIGMA",
    "ERROR",
    "FiniteStateMachine"
)

EPSILON = "EPSILON"
SIGMA = "SIGMA"
ERROR = "ERROR"

ElementType = TypeVar("ElementType")


class FiniteStateMachine(Generic[ElementType]):
    """Finite State Machine implementation.

    This implementation supports multiple current states and Epsilon
    transitions.

    Attributes:
        initial_states (set of int): Initial states of the FSM: the FSM will
            start at these states.
        final_states (set of int): Final states of the FSM: the FSM will accept
            a sequence of ElementType if at least one of the last states is 
            contained in this set.
        default_states (set of int): Default (or error) states of the FSM: the
            FSM will go to these states if there is no transition defined for
            the current element and state.
    """

    initial_states: Set[int]
    final_states: Set[int]
    default_states: Set[int]
    transitions: Dict[ElementType, Dict[int, Set[int]]]

    def __init__(
            self,
            initial_states: Set[int] = None,
            final_states: Set[int] = None,
            default_states: Set[int] = None
    ):
        super().__init__()
        self.initial_states = set() if initial_states is None else initial_states
        self.final_states = set() if final_states is None else final_states
        self.default_states = set() if default_states is None else default_states
        self.transitions = {}

    def __contains__(self, state: int) -> bool:
        return self.has_state(state)

    def __setitem__(self, state: int, connections: Dict[ElementType, Set[int]]):
        self.add_state(state, connections)

    def __getitem__(self, state: int) -> Dict[ElementType, Set[int]]:
        return self.get_state(state)

    def __delitem__(self, state: int):
        self.remove_state(state)

    @property
    def input_set(self) -> Set[ElementType]:
        """set of ElementType: All the input elements used in the FSM."""
        return set(self.transitions)

    @property
    def state_set(self) -> Set[int]:
        """set of int: All the states used in the FSM"""
        state_set = set()
        for connections in self.transitions.values():
            for from_state, to_states in connections.items():
                state_set.update(to_states | {from_state})
        return state_set | self.initial_states | self.default_states | self.final_states

    def add_initial_states(
            self,
            initial_states: Set[int]
    ):
        """Add states to the initial states of the FSM."""
        self.initial_states.update(initial_states)

    def remove_initial_states(
            self,
            initial_states: Set[int] = None
    ):
        """Removes states from the initial states of the FSM."""
        if initial_states is not None:
            self.initial_states.difference_update(initial_states)
        else:
            self.initial_states.clear()

    def add_final_states(
            self,
            final_states: Set[int]
    ):
        """Adds states to the final states of the FSM."""
        self.final_states.update(final_states)

    def remove_final_states(
            self,
            final_states: Set[int] = None
    ):
        """Removes states from the final states of the FSM."""
        if final_states is not None:
            self.final_states.difference_update(final_states)
        else:
            self.final_states.clear()

    def add_default_states(
            self,
            default_states: Set[int]
    ):
        """Adds states to the default states of the FSM."""
        self.default_states.update(default_states)

    def remove_default_states(
            self,
            default_states: Set[int] = None
    ):
        """Removes states from the default states of the FSM."""
        if default_states is not None:
            self.default_states.difference_update(default_states)
        else:
            self.default_states.clear()

    def has_transition(
            self,
            element: ElementType,
            from_state: int,
            to_states: Set[int] = None
    ) -> bool:
        """bool: Checks if a specific transition is defined in the FSM."""
        context = element in self.transitions and from_state in self.transitions[element]
        if context:
            return context and (
                to_states in self.transitions[element][from_state]
                if to_states is not None
                else True
            )

    def add_transition(
            self,
            element: ElementType,
            from_state: int,
            to_states: Set[int]
    ):
        """Adds a transition to the FSM."""
        if self.has_transition(element, from_state):
            self.transitions[element][from_state].update(to_states)
        elif element in self.input_set:
            self.transitions[element][from_state] = to_states
        else:
            self.transitions[element] = {from_state: to_states}

    def get_transition(
            self,
            element: ElementType,
            from_state: int
    ) -> Set[int]:
        """Returns a transition defined in the FSM."""
        if self.has_transition(element, from_state):
            return self.transitions[element][from_state]
        return self.default_states

    def remove_transition(
            self,
            element: ElementType,
            from_state: int,
            to_states: Set[int] = None
    ):
        """Removes a transition from the FSM."""
        assert self.has_transition(element, from_state, to_states)
        if to_states is not None:
            self.transitions[element][from_state].difference_update(to_states)
        pointer = self.transitions[element][from_state]
        if to_states is None or not pointer:
            del pointer

    def has_state(
            self,
            state: int
    ) -> bool:
        """bool: Checks if a specific state is defined in the FSM."""
        return any(
            state in to_states or state == from_state
            for connections in self.transitions.values()
            for from_state, to_states in connections.items()
        )

    def add_state(
            self,
            state: int,
            connections: Dict[ElementType, Set[int]]
    ):
        """Adds a state and its connections to the FSM."""
        for element, to_states in connections.items():
            self.add_transition(element, state, to_states)

    def get_state(
            self,
            state: int
    ) -> Dict[ElementType, Set[int]]:
        """dict of ElementType and set of int: Returns the connections of a 
            state in the FSM."""
        connections = {}
        for element, connection in self.transitions.items():
            for from_state, to_states in connection.items():
                if state == from_state:
                    connections[element] = to_states
        return connections

    def remove_state(
            self,
            state: int
    ):
        """Removes a state and its connections from the FSM."""
        assert self.has_state(state)
        for element in self.transitions:
            for from_state, to_states in self.transitions[element].items():
                if state in to_states:
                    self.remove_transition(element, from_state, {state})
                if from_state == state:
                    del self.transitions[element][state]
                pointer = self.transitions[element]
                if not pointer:
                    del pointer

    def run(
            self,
            sequence: Sequence[ElementType],
            error_on_default: bool = True
    ) -> Iterator[Tuple[int, ElementType, Set[int]]]:
        """iter of tuple of ElementType and set of int: Iterates the FSM through
            the sequence of ElementType."""
        current_states = self.initial_states
        position = 0
        while position < len(sequence):
            new_states = set()
            if error_on_default and current_states == self.default_states:
                yield position, ERROR, self.default_states
                return
            for state in current_states:
                connections = self.get_state(state)
                if EPSILON in connections and current_states & connections[EPSILON] != connections[EPSILON]:
                    current_states.update(connections[EPSILON])
                    yield position, EPSILON, current_states
                    break
                if SIGMA in connections:
                    new_states.update(connections[SIGMA])
                for element in connections.keys():
                    if type(element) is frozenset and sequence[position] in element:
                        new_states.update(connections[element])
                new_states.update(self.get_transition(sequence[position], state))
            else:
                current_states = new_states
                yield position, sequence[position], current_states
                position += 1

    def last(
            self,
            sequence: Sequence[ElementType],
            error_on_default: bool = True
    ) -> Set[int]:
        """set of int: Returns the last states of iterating the sequence of 
            ElementType though the FSM."""
        last_states = set()
        for position, _, last_states in self.run(sequence, error_on_default):
            pass
        return last_states

    def accepts(
            self,
            sequence: Sequence[ElementType],
            error_on_default: bool = True
    ) -> Set[int]:
        """set of int: Returns the last states contained in the final states of
            the FSM after iterating through the sequence of ElementType."""
        return self.final_states & self.last(sequence, error_on_default)
