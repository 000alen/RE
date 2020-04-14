from typing import TypeVar, Generic, Set, Dict, List, Iterator, Tuple


ElementType = TypeVar('ElementType')


class FiniteStateMachine(Generic[ElementType]):
    initial_states: Set[int]
    final_states: Set[int]
    default_states: Set[int]

    transitions: Dict[ElementType, Dict[int, Set[int]]]

    def __init__(
        self,
        initial_states: Set[int] = set(),
        final_states: Set[int] = set(),
        default_states: Set[int] = set()
    ):
        super().__init__()
        self.initial_states = initial_states
        self.final_states = final_states
        self.default_states = default_states
        self.transitions = {}

    # Properties
    @property
    def InputSet(self) -> Set[ElementType]:
        return set(self.transitions)

    @property
    def StateSet(self) -> Set[int]:
        pass

    # Initial State Operations
    @property
    def InitialStates(self) -> Set[int]:
        return self.initial_states

    def AddInitialStates(
        self,
        initial_states: Set[int]
    ):
        self.initial_states.update(initial_states)

    def RemoveInitialStates(
        self,
        initial_states: Set[int] = None
    ):
        if initial_states is not None:
            self.initial_states.difference_update(initial_states)
        else:
            self.initial_states.clear()

    # Final State Operations
    @property
    def FinalStates(self) -> Set[int]:
        return self.final_states

    def AddFinalStates(
        self,
        final_states: Set[int]
    ):
        self.final_states.update(final_states)

    def RemoveFinalStates(
        self,
        final_states: Set[int] = None
    ):
        if final_states is not None:
            self.final_states.difference_update(final_states)
        else:
            self.final_states.clear()

    # Default State Operations
    @property
    def DefaultStates(self) -> Set[int]:
        return self.default_states

    def AddDefaultStates(
        self,
        default_states: Set[int]
    ):
        self.default_states.update(default_states)

    def RemoveDefaultStates(
        self,
        default_states: Set[int] = None
    ):
        if default_states is not None:
            self.default_states.difference_update(default_states)
        else:
            self.default_states.clear()

    # Transition Operations
    def HasTransition(
        self,
        element: ElementType,
        from_state: int,
        to_states: Set[int] = None
    ) -> bool:
        if (context := element in self.transitions and from_state in self.transitions[element]):
            return context and (
                to_states in self.transitions[element][from_state]
                if to_states is not None
                else True
            )

    def AddTransition(
        self,
        element: ElementType,
        from_state: int,
        to_states: Set[int]
    ):
        if self.HasTransition(element, from_state):
            self.transitions[element][from_state].update(to_states)
        elif element in self.InputSet:
            self.transitions[element][from_state] = to_states
        else:
            self.transitions[element] = {from_state: to_states}

    def GetTransition(
        self,
        element: ElementType,
        from_state: int
    ) -> Set[int]:
        if self.HasTransition(element, from_state):
            return self.transitions[element][from_state]
        return self.default_states

    def RemoveTransition(
        self,
        element: ElementType,
        from_state: int,
        to_states: Set[int] = None
    ):
        assert self.HasTransition(element, from_state, to_states)
        if to_states is not None:
            self.transitions[element][from_state].difference_update(to_states)
        if to_states is None or not (pointer := self.transitions[element][from_state]):
            del pointer

    # State Operations
    def HasState(
        self,
        state: int
    ) -> bool:
        return any(
            state in to_states or state == from_state
            for from_state, to_states in connections.items()
            for connections in self.transitions.values()
        )

    def AddState(
        self,
        state: int,
        connections: Dict[ElementType, Set[int]]
    ):
        for element, to_states in connections.items():
            self.AddTransition(element, state, to_states)

    def GetState(
        self,
        state: int
    ) -> Dict[ElementType, Set[int]]:
        return {
            element: to_states
            for from_state, to_states in self.transitions[element].items()
            if from_state == state
            for element in self.transitions
        }

    def RemoveState(
        self,
        state: int
    ):
        assert self.HasState(state)  
        for element in self.transitions:
            for from_state, to_states in self.transitions[element].items():
                if state in to_states:
                    self.RemoveTransition(element, from_state, state)
                if from_state == state:
                    del self.transitions[element][state]
                if not (pointer := self.transitions[element]):
                    del pointer

    # Operations
    def Run(
        self,
        sequence: List[ElementType]
    ) -> Iterator[Tuple[ElementType, Set[int]]]:
        current_states = self.initial_states
        for element in sequence:
            new_states = set()
            for state in current_states:
                new_states.update(self.GetTransition(element, state))
            current_states = new_states
            yield element, current_states

    def Last(
        self,
        sequence: List[ElementType]
    ) -> Set[input]:
        for _, last_states in self.Run(sequence):
            pass
        return last_states

    def Accept(
        self,
        sequence: List[ElementType]
    ) -> Set[int]:
        return self.final_states.intersection(self.Last(sequence))
