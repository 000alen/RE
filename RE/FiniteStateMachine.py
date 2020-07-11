from typing import Dict, Generic, Iterator, List, Set, Tuple, TypeVar


EPSILON = "EPSILON"

ElementType = TypeVar("ElementType")


class FiniteStateMachine(Generic[ElementType]):
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
        if initial_states is None:
            initial_states = set()
        if final_states is None:
            final_states = set()
        if default_states is None:
            default_states = set()
        self.initial_states = initial_states
        self.final_states = final_states
        self.default_states = default_states
        self.transitions = {}

    @property
    def input_set(self) -> Set[ElementType]:
        return set(self.transitions)

    @property
    def state_set(self) -> Set[int]:
        # TODO: Refactor
        state_set = set()
        for _ in self.transitions.values():
            for from_state, to_states in _.items():
                state_set.update(to_states.union({from_state}))
        return state_set.union(self.initial_states, self.default_states, self.final_states)

    def add_initial_states(
        self,
        initial_states: Set[int]
    ):
        self.initial_states.update(initial_states)

    def remove_initial_states(
        self,
        initial_states: Set[int] = None
    ):
        if initial_states is not None:
            self.initial_states.difference_update(initial_states)
        else:
            self.initial_states.clear()

    def add_final_states(
        self,
        final_states: Set[int]
    ):
        self.final_states.update(final_states)

    def remove_final_states(
        self,
        final_states: Set[int] = None
    ):
        if final_states is not None:
            self.final_states.difference_update(final_states)
        else:
            self.final_states.clear()

    def add_default_states(
        self,
        default_states: Set[int]
    ):
        self.default_states.update(default_states)

    def remove_default_states(
        self,
        default_states: Set[int] = None
    ):
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
        if self.has_transition(element, from_state):
            return self.transitions[element][from_state]
        return self.default_states

    def remove_transition(
        self,
        element: ElementType,
        from_state: int,
        to_states: Set[int] = None
    ):
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
        return any(
            state in to_states or state == from_state
            for from_state, to_states in connections.items()
            for connections in self.transitions.values()
        )

    def add_state(
        self,
        state: int,
        connections: Dict[ElementType, Set[int]]
    ):
        for element, to_states in connections.items():
            self.add_transition(element, state, to_states)

    def get_state(
        self,
        state: int
    ) -> Dict[ElementType, Set[int]]:
        # return {
        #     element: to_states
        #     for from_state, to_states in self.transitions[element].items()
        #     if from_state == state
        #     for element in self.transitions
        # }
        x = {}
        for element, connection in self.transitions.items():
            for from_state, to_states in connection.items():
                if state == from_state:
                    x[element] = to_states
        return x

    def remove_state(
        self,
        state: int
    ):
        assert self.has_state(state)
        for element in self.transitions:
            for from_state, to_states in self.transitions[element].items():
                if state in to_states:
                    self.remove_transition(element, from_state, state)
                if from_state == state:
                    del self.transitions[element][state]
                pointer = self.transitions[element]
                if not pointer:
                    del pointer

    def run(
        self,
        sequence: List[ElementType]
    ) -> Iterator[Tuple[ElementType, Set[int]]]:
        current_states = self.initial_states
        i = 0
        while i < len(sequence):
            new_states = set()
            for state in current_states:
                connections = self.get_state(state)
                if EPSILON in connections and connections[EPSILON] not in current_states:
                    current_states.update(connections[EPSILON])
                    yield EPSILON, current_states
                    continue
                new_states.update(self.get_transition(sequence[i], state))
            current_states = new_states
            yield sequence[i], current_states
            i += 1

    def last(
        self,
        sequence: List[ElementType]
    ) -> Set[input]:
        for _, last_states in self.run(sequence):
            pass
        return last_states

    def accepts(
        self,
        sequence: List[ElementType]
    ) -> Set[int]:
        return self.final_states.intersection(self.last(sequence))
