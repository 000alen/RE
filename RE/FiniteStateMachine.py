# TODO: Deprecate usage of RE.FiniteStateMachine.Symbol.SIGMA

from enum import Enum, auto
from typing import Dict, Iterator, Set, Tuple, FrozenSet, Union

__all__ = (
    "Symbol",
    "FiniteStateMachine"
)

KeyType = Union["Symbol", str, FrozenSet[str]]
ConnectionsType = Dict[KeyType, FrozenSet[int]]


class Symbol(Enum):
    """TODO
    """

    EPSILON = auto()
    SIGMA = auto()
    EOF = auto()


class FiniteStateMachine:
    """Finite State Machine implementation.

    This implementation supports multiple current states and Epsilon transitions.

    Attributes: initial_states (set of int): Initial states of the FSM: the FSM will start at these states.
    final_states (set of int): Final states of the FSM: the FSM will accept a sequence of ElementType if at least one
        of the last states is contained in this set.

    Structures:
        connections (dict of KeyType and Set of int):
        transitions (set of int)
    """

    initial_states: Set[int]
    final_states: Set[int]
    transitions: Dict[KeyType, Dict[int, Set[int]]]

    def __init__(
            self,
            initial_states: Set[int] = None,
            final_states: Set[int] = None
    ):
        super().__init__()
        self.initial_states = set() if initial_states is None else initial_states
        self.final_states = set() if final_states is None else final_states
        self.transitions = {}

    def __contains__(self, state: int) -> bool:
        return state in self.state_set

    def __setitem__(self, state: int, connections: ConnectionsType):
        self.add_connections(state, connections)

    def __getitem__(self, state: int) -> ConnectionsType:
        return self.get_connections(state)

    def __delitem__(self, state: int):
        self.remove_connections(state)

    def __call__(self, string: str) -> Iterator[Tuple[KeyType, FrozenSet[int]]]:
        return self.run(string)

    @property
    def input_set(self) -> FrozenSet[KeyType]:
        """frozenset of KeyType: All the input elements used in the FSM."""
        return frozenset(self.transitions.keys())

    @property
    def state_set(self) -> FrozenSet[int]:
        """frozenset of int: All the states used in the FSM."""
        state_set = set()
        for transitions in self.transitions.values():
            for from_state, to_states in transitions.items():
                state_set.update({from_state} | to_states)
        return frozenset(state_set | self.initial_states | self.final_states)

    def add_initial_states(
            self,
            initial_states: Set[int]
    ):
        """Adds states to the initial states of the FSM."""
        self.initial_states.update(initial_states)

    def remove_initial_states(
            self,
            initial_states: Set[int] = None
    ):
        """Removes states from the initial states of the FSM."""
        if initial_states is None:
            self.initial_states.clear()
        else:
            self.initial_states.difference_update(initial_states)

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
        if final_states is None:
            self.final_states.clear()
        else:
            self.final_states.difference_update(final_states)

    def has_transition(
            self,
            element: KeyType,
            from_state: int,
            to_states: Set[int] = None
    ) -> bool:
        """bool: Checks if a transition is defined in the FSM."""
        return (
                element in self.transitions
                and from_state in self.transitions[element]
                and (
                    True
                    if to_states is None
                    else to_states == self.transitions[element][from_state]
                )
        )

    def add_transition(
            self,
            element: KeyType,
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
            element: KeyType,
            from_state: int
    ) -> FrozenSet[int]:
        """frozenset of int: Returns a transition defined in the FSM."""
        assert self.has_transition(element, from_state)
        return frozenset(self.transitions[element][from_state])

    def remove_transition(
            self,
            element: KeyType,
            from_state: int,
            to_states: Set[int] = None
    ):
        """Removes a transition from the FSM."""
        assert self.has_transition(element, from_state, to_states)
        if to_states is None:
            del self.transitions[element][from_state]
        else:
            self.transitions[element][from_state].difference_update(to_states)

    def add_connections(
            self,
            state: int,
            connections: ConnectionsType
    ):
        """Adds a state and its connections to the FSM."""
        for element, to_states in connections.items():
            self.add_transition(element, state, set(to_states))

    def get_connections(
            self,
            state: int
    ) -> ConnectionsType:
        """ConnectionsType: Returns the connections of a state in the FSM."""
        assert state in self.state_set
        connections = {}
        for element, transition in self.transitions.items():
            for from_state, to_states in transition.items():
                if state == from_state:
                    connections[element] = frozenset(to_states)
        return connections

    def remove_connections(
            self,
            state: int
    ):
        """Removes a state and its connections from the FSM."""
        assert state in self.state_set
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
            string: str
    ) -> Iterator[Tuple[KeyType, FrozenSet[int]]]:
        """iter of tuple of str and frozenset of int: Iterates the str through the FSM."""

        def _current_states() -> Iterator[int]:
            _state = current_states.pop() if current_states else None
            while _state is not None:
                yield _state
                _state = current_states.pop() if current_states else None

        current_states = self.initial_states.copy()
        new_states = set()
        for element in (*string, Symbol.EOF):
            new_states = current_states.copy() if element is Symbol.EOF else new_states
            for state in _current_states():
                connections = self.get_connections(state)
                if Symbol.EPSILON in connections:
                    current_states.update(connections[Symbol.EPSILON] - {state})
                    if element is Symbol.EOF:
                        new_states.update(connections[Symbol.EPSILON])
                if element is not Symbol.EOF:
                    if Symbol.SIGMA in connections:
                        new_states.update(connections[Symbol.SIGMA])
                    if element in connections:
                        new_states.update(connections[element])
                    if any(type(_) is frozenset for _ in connections.keys()):
                        for element_set in connections.keys():
                            if type(element_set) is frozenset and element in element_set:
                                new_states.update(connections[element_set])
            if element is Symbol.EOF and not new_states:
                break
            current_states.update(new_states)
            new_states.clear()
            yield element, frozenset(current_states)
            if not current_states:
                break

    def last(
            self,
            string: str
    ) -> FrozenSet[int]:
        """frozenset of int: Returns the last states of iterating the str through the FSM."""
        last_states = None
        for element, last_states in self.run(string):
            pass
        return last_states

    def accepts(
            self,
            string: str
    ) -> bool:
        """bool: Returns True if the at least one of the last states is a final states after iterating the str through
            the FSM. """
        return bool(self.final_states & self.last(string))
